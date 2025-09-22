from helpers.response_callback import ResponseCallback
from langchain.chat_models import init_chat_model
from langgraph.graph import StateGraph, START, END
from typing import TypedDict, List, Callable
from graphs.reconnaissance_graph import reconnaissance_graph
from graphs.planning_graph import planning_graph, PlanItem
from helpers.cached import cached


class State(TypedDict):
    base_url: str
    reconnaissance: str
    plan: List[PlanItem]


def reconnoitre(state: State):
    subgraph_output = cached("reconnaissance", reconnaissance_graph.invoke)(
        {"base_url": state["base_url"]}
    )
    return {"reconnaissance": subgraph_output["reconnaissance"]}


def plan(state: State):
    subgraph_output = cached("plan", planning_graph.invoke)(
        {"base_url": state["base_url"], "reconnaissance": state["reconnaissance"]}
    )
    return {"plan": subgraph_output["plan"]}


llm = init_chat_model("anthropic:claude-sonnet-4-20250514", max_tokens=8192)

graph_builder = StateGraph(State)
graph_builder.add_node("reconnaissance", reconnoitre)
graph_builder.add_node("plan", plan)

graph_builder.add_edge(START, "reconnaissance")
graph_builder.add_edge("reconnaissance", "plan")
graph_builder.add_edge("plan", END)

graph = graph_builder.compile()

# print(graph.get_graph(xray=1).draw_mermaid())

graph.invoke(
    {"base_url": "http://localhost:3000"},
    {"recursion_limit": 100, "callbacks": [ResponseCallback()]},
)
