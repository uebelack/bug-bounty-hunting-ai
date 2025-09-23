import requests
from langchain_core.tools import tool
from langgraph.prebuilt import tools_condition, ToolNode
from graphs.planning_graph import Task
from langchain_core.messages import SystemMessage, HumanMessage
from langchain_core.language_models.chat_models import BaseChatModel
from langgraph.graph import StateGraph, START, END, MessagesState
from graphs.reporting_graph import create_reporting_graph
from typing import List
from graphs.reporting_graph import Report


@tool
def http_request(url: str, method: str, headers: dict = None, data: str = None):
    """Make an HTTP request to the specified URL with the given method, headers, and data."""
    response = requests.request(method, url, headers=headers, data=data)

    # Limit response size to avoid token limit issues
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


class ExecutionState(MessagesState):
    base_url: str
    task: Task
    result: str
    reports: List[Report]


SYSTEM_PROMPT = """
You are a bug bounty hunter part of a team of bug bounty hunters.
The reconnaissance team has already completed the reconnaissance phase and
the planning team has already created a test plan.
Your job is to execute one of the test plan items and find vulnerabilities in the target website.
You will use the tools provided to you to execute the test plan item.
"""


def create_execution_graph(llm: BaseChatModel):
    tools = [http_request]
    llm_with_tools = llm.bind_tools(tools)
    reporting_graph = create_reporting_graph(llm)

    def execute_task(state: ExecutionState):
        print(f"🛠️ Executing ...")

        prompt = f"""Task: 
{state['task'].title}
{state['task'].instructions}

Target website:
{state['base_url']}

Please execute the task and find vulnerabilities in the target website.
Use the tools provided to you to execute the task.
Finish with a details report of the vulnerabilities you found.
"""

        response = llm_with_tools.invoke(
            [
                SystemMessage(content=SYSTEM_PROMPT),
                HumanMessage(content=prompt),
            ]
            + state["messages"]
        )
        return {"messages": response}

    def store_result(state: ExecutionState):
        result = state["messages"][-1].content
        return {"result": result}

    graph_builder = StateGraph(ExecutionState)
    graph_builder.add_node("execute_task", execute_task)
    graph_builder.add_node("tools", ToolNode(tools))
    graph_builder.add_node("store_result", store_result)
    graph_builder.add_node("report", reporting_graph)

    graph_builder.add_edge(START, "execute_task")
    graph_builder.add_conditional_edges(
        "execute_task",
        tools_condition,
        {"tools": "tools", END: "store_result"},
    )
    graph_builder.add_edge("tools", "execute_task")
    graph_builder.add_edge("store_result", "report")
    graph_builder.add_edge("report", END)

    return graph_builder.compile()
