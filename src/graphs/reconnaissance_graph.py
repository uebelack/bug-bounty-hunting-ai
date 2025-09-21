from langchain_core.prompts import prompt
from helpers.response_callback import ResponseCallback
from langchain_community.agent_toolkits.openapi.toolkit import RequestsToolkit
from langchain_community.utilities.requests import TextRequestsWrapper
from langchain_core.messages import SystemMessage, HumanMessage, BaseMessage
from langchain_core.tools import tool
from langchain.chat_models import init_chat_model
from langgraph.graph import StateGraph, START, END, MessagesState
from langgraph.prebuilt import tools_condition, ToolNode
from wappalyzer import analyze

import json

http_tools = RequestsToolkit(
    requests_wrapper=TextRequestsWrapper(headers={}),
    allow_dangerous_requests=True,
).get_tools()


@tool
def wappalyzer(url: str):
    """
    Wappalyzer identifies technologies on a website, such as CMS, web frameworks,
    ecommerce platforms, JavaScript libraries, analytics tools etc.
    """
    print(f"🛠️ Wappalyzer: analyzing website {url}")

    return json.dumps(analyze(url))


class State(MessagesState):
    base_url: str
    reconnaissance: str


llm = init_chat_model("anthropic:claude-sonnet-4-20250514", max_tokens=8192)


# Reconnaissance Phase - gather information about the target website
tools = [wappalyzer, *http_tools]
llm = llm.bind_tools([wappalyzer, *http_tools])
graph_builder = StateGraph(State)


def reconnoitre(state: State):
    print(f"🛠️ Reconnoitre ...")
    response = llm.invoke(
        [
            SystemMessage(
                content="You are a passive reconnaissance assistant for a bug-bounty engagement. \
                    Only perform passive OSINT; do not run active scans or exploit attempts. \
                    Produce: \
                    1) executive summary, \
                    2) asset inventory (CSV), \
                    3) prioritized findings table (no exploit steps), \
                    4) sources/evidence list, \
                    5) recommended safe next steps. \
                    Log all sources and timestamps."
            ),
            HumanMessage(content=f"The target website is {state['base_url']}."),
        ]
        + state["messages"]
    )
    return {"messages": response}


def store_reconnaissance(state: State):
    print(f"🛠️ Storing reconnaissance ...")
    return {"reconnaissance": state["messages"][-1].content}


graph_builder.add_node("reconnoitre", reconnoitre)
graph_builder.add_node("tools", ToolNode(tools))
graph_builder.add_node("store_reconnaissance", store_reconnaissance)

graph_builder.add_edge(START, "reconnoitre")
graph_builder.add_conditional_edges("reconnoitre", tools_condition)
graph_builder.add_edge("tools", "reconnoitre")
graph_builder.add_edge("reconnoitre", "store_reconnaissance")
graph_builder.add_edge("store_reconnaissance", END)

reconnaissance_graph = graph_builder.compile()
