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
from typing_extensions import TypedDict
from typing import List
from pydantic import BaseModel, Field

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


class PlanItem(BaseModel):
    title: str = Field(
        description="Descriptive title for this specific testing phase or security assessment task (e.g., 'Directory Enumeration', 'Authentication Testing', 'Input Validation Analysis')",
    )
    prompt: str = Field(
        description="Detailed instruction prompt that guides the agent on how to execute this specific testing phase, including objectives, methodologies, tools to use, success criteria, and expected deliverables",
    )


class Plan(BaseModel):
    plan: List[PlanItem] = Field(
        description="Ordered sequence of security testing phases and assessment tasks to be executed during the bug bounty engagement, prioritized by risk level and logical testing progression (reconnaissance → enumeration → vulnerability assessment → exploitation → post-exploitation)",
    )


class State(MessagesState):
    base_url: str
    reconnaissance: str
    plan: Plan


graph_builder = StateGraph(State)

llm = init_chat_model("anthropic:claude-sonnet-4-20250514")

reconnaissance_tools = [wappalyzer, *http_tools]
reconnaissance_llm = llm.bind_tools([wappalyzer, *http_tools])


# Reconnoitre Phase - gather information about the target website
def reconnoitre(state: State):
    print(f"🛠️ Reconnoitre ...")
    response = reconnaissance_llm.invoke(
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


def save_reconnaissance(state: State):
    print(f"🛠️ Saving reconnaissance")
    return {"reconnaissance": state["messages"][-1].content}


def plan(state: State):
    print(f"🛠️ Planning ...")
    response = llm.with_structured_output(Plan).invoke(
        [
            SystemMessage(
                content="You are a planning assistant for an authorized bug-bounty engagement. \
                    Given recon inputs (asset inventory, findings), produce a safe, prioritized \
                    test plan and scenarios that contain objectives, preconditions, allowed techniques \
                    (passive / authorized active / authenticated), success criteria, required evidence, \
                    ROE, and mitigation guidance — do not include exploit steps or payloads"
            ),
            HumanMessage(content=f"The target website is {state['base_url']}."),
        ]
    )
    return {"plan": response}


graph_builder.add_node("reconnoitre", reconnoitre)
graph_builder.add_node("tools", ToolNode(reconnaissance_tools))
graph_builder.add_node("save_reconnaissance", save_reconnaissance)
graph_builder.add_node("plan", plan)

graph_builder.add_edge(START, "reconnoitre")
graph_builder.add_conditional_edges(
    "reconnoitre", tools_condition, {"tools": "tools", "__end__": "save_reconnaissance"}
)
graph_builder.add_edge("tools", "reconnoitre")
graph_builder.add_edge("save_reconnaissance", "plan")
graph_builder.add_edge("plan", END)

graph = graph_builder.compile()

# store graph in png

image = graph.get_graph().draw_mermaid_png()

with open("graph.png", "wb") as f:
    f.write(image)


graph.invoke(
    {"base_url": "http://localhost:3000"},
    {"recursion_limit": 100, "callbacks": [ResponseCallback()]},
)
