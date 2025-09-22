from langgraph.prebuilt import tools_condition, ToolNode
from graphs.planning_graph import Task
from langchain_community.agent_toolkits.openapi.toolkit import RequestsToolkit
from langchain_community.utilities.requests import TextRequestsWrapper
from langchain_core.messages import SystemMessage, HumanMessage, AIMessage, ToolMessage
from langchain_core.language_models.chat_models import BaseChatModel
from langgraph.graph import StateGraph, START, END, MessagesState
from typing import List
from pydantic import BaseModel, Field

http_tools = RequestsToolkit(
    requests_wrapper=TextRequestsWrapper(headers={}),
    allow_dangerous_requests=True,
).get_tools()


class Report(BaseModel):
    title: str = Field(
        description="Concise title of the finding (e.g., 'SQL Injection in login endpoint')",
    )
    description: str = Field(
        description="Detailed description of the finding, including background and affected functionality",
    )
    impact: str = Field(
        description="Business or technical impact of the finding (e.g., data leakage, privilege escalation)",
    )
    severity: str = Field(
        description="Severity rating of the finding (e.g., Low, Medium, High, Critical)",
    )
    steps_to_reproduce: List[str] = Field(
        description="Step-by-step guide to reproduce the issue",
    )
    recommendations: str = Field(
        description="Security recommendations and mitigation steps",
    )


class Reports(BaseModel):
    reports: List[Report] = Field(
        description="List of reports",
    )


class ExecutionState(MessagesState):
    base_url: str
    reconnaissance: str
    task: Task
    index: int = 0


SYSTEM_PROMPT = """
You are a bug bounty hunter part of a team of bug bounty hunters.
The reconnaissance team has already completed the reconnaissance phase and
the planning team has already created a test plan.
Your job is to execute one of the test plan items and find vulnerabilities in the target website.
You will use the tools provided to you to execute the test plan item.
"""


def create_execution_graph(llm: BaseChatModel):
    tools = [*http_tools]
    llm_with_tools = llm.bind_tools(tools)

    def execute_task(state: ExecutionState):
        print(f"🛠️ Executing ...")

        prompt = f"""Task: 
{state['task'].title}
{state['task'].instructions}

Reconnaissance:
{state['reconnaissance']}

Target website:
{state['base_url']}

Please execute the task and find vulnerabilities in the target website.
You will report the vulnerabilities you find to the team.
Use the tools provided to you to execute the task.
"""

        response = llm_with_tools.invoke(
            [
                SystemMessage(content=SYSTEM_PROMPT),
                HumanMessage(content=prompt),
            ]
            + state["messages"]
        )
        return {"messages": response}

    def create_report(state: ExecutionState):
        structured_llm_with_tools = llm.with_structured_output(Reports)
        response = structured_llm_with_tools.invoke(
            state["messages"]
            + [
                HumanMessage(
                    content="Please create a structured report for each vulnerability you found."
                )
            ]
        )
        return {"reports": response.reports}

    graph_builder = StateGraph(ExecutionState)
    graph_builder.add_node("execute_task", execute_task)
    graph_builder.add_node("tools", ToolNode(tools))
    graph_builder.add_node("create_report", create_report)

    graph_builder.add_edge(START, "execute_task")
    graph_builder.add_conditional_edges(
        "execute_task",
        tools_condition,
        {
            "tools": "tools",
            "end": "create_report",
        },
    )
    graph_builder.add_edge("tools", "execute_task")
    graph_builder.add_edge("create_report", END)

    return graph_builder.compile()
