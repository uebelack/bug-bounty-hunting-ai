from helpers.response_callback import ResponseCallback
from langchain_community.agent_toolkits.openapi.toolkit import RequestsToolkit
from langchain_community.utilities.requests import TextRequestsWrapper
from langchain_core.messages import SystemMessage, HumanMessage
from langchain_core.tools import tool
from langchain.chat_models import init_chat_model
from langgraph.graph import StateGraph, START, MessagesState
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


graph_builder = StateGraph(State)

llm = init_chat_model("anthropic:claude-sonnet-4-20250514")

reconnaissance_tools = [wappalyzer, *http_tools]
reconnaissance_llm = llm.bind_tools([wappalyzer, *http_tools])


def reconnoitre(state: State):
    response = reconnaissance_llm.invoke(
        [
            SystemMessage(
                content="You are a passive reconnaissance assistant for an authorized bug-bounty engagement. \
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


graph_builder.add_node("reconnoitre", reconnoitre)
graph_builder.add_node("tools", ToolNode(reconnaissance_tools))
graph_builder.add_edge(START, "reconnoitre")
graph_builder.add_conditional_edges(
    "reconnoitre",
    tools_condition,
)
graph_builder.add_edge("tools", "reconnoitre")
graph = graph_builder.compile()


graph.invoke(
    {"base_url": "http://localhost:3000"},
    {"recursion_limit": 100, "callbacks": [ResponseCallback()]},
)
