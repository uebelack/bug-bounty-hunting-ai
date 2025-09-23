import requests
from langchain_core.tools import tool
from langgraph.prebuilt import tools_condition, ToolNode
from graphs.planning_graph import Task
from langchain_community.agent_toolkits.openapi.toolkit import RequestsToolkit
from langchain_community.utilities.requests import TextRequestsWrapper
from langchain_core.messages import SystemMessage, HumanMessage
from langchain_core.language_models.chat_models import BaseChatModel
from langgraph.graph import StateGraph, START, END, MessagesState
from typing import List
from pydantic import BaseModel, Field

http_tools = RequestsToolkit(
    requests_wrapper=TextRequestsWrapper(headers={}),
    allow_dangerous_requests=True,
).get_tools()


@tool
def upload(
    url: str,
    filename: str,
    content: str,
    additional_data: dict = None,
    headers: dict = None,
) -> str:
    """Upload a file to the target website"""

    files = {filename: content}
    response = requests.post(
        url, files=files, data=additional_data or {}, headers=headers or {}, timeout=30
    )

    max_response_length = 50000

    raw_response = (
        f"HTTP/{response.raw.version/10:.1f} {response.status_code} {response.reason}\n"
    )
    for header, value in response.headers.items():
        raw_response += f"{header}: {value}\n"
    raw_response += "\n"

    # Truncate response body if too long
    response_text = response.text
    if len(response_text) > max_response_length:
        response_text = (
            response_text[:max_response_length]
            + f"\n\n[Response truncated - showing first {max_response_length} characters]"
        )

    raw_response += response_text

    return raw_response


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
    task: Task
    reports: List[Report]
    index: int = 0


SYSTEM_PROMPT = """
You are a bug bounty hunter part of a team of bug bounty hunters.
The reconnaissance team has already completed the reconnaissance phase and
the planning team has already created a test plan.
Your job is to execute one of the test plan items and find vulnerabilities in the target website.
You will use the tools provided to you to execute the test plan item.
Please create a report directly after you have found a vulnerability and 
then continue looking for more vulnerabilities, so that we can remove the earlier tool 
responses from the conversation history.
"""


def create_execution_graph(llm: BaseChatModel):
    tools = [*http_tools, upload]
    llm_with_tools = llm.bind_tools(tools)

    def execute_task(state: ExecutionState):
        print(f"🛠️ Executing ...")

        prompt = f"""Task: 
{state['task'].title}
{state['task'].instructions}

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
            END: "create_report",
        },
    )
    graph_builder.add_edge("tools", "execute_task")
    graph_builder.add_edge("create_report", END)

    return graph_builder.compile()
