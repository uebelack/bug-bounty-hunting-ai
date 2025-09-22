from helpers.response_callback import ResponseCallback
from langchain.chat_models import init_chat_model
from langgraph.graph import StateGraph, START, END
from typing import TypedDict, List
from graphs.reconnaissance_graph import create_reconnaissance_graph
from graphs.planning_graph import create_planning_graph, Task
from graphs.execution_graph import create_execution_graph
from helpers.cached import cached

llm = init_chat_model("anthropic:claude-sonnet-4-20250514", max_tokens=8192)
reconnaissance_graph = create_reconnaissance_graph(llm)
planning_graph = create_planning_graph(llm)
execution_graph = create_execution_graph(llm)


class State(TypedDict):
    base_url: str
    reconnaissance: str
    plan: List[Task]
    plan_index: int
    reports: List[str]


# Reconnaissance Phase - gather information about the target website
def reconnoitre(state: State):
    subgraph_output = cached("reconnaissance", reconnaissance_graph.invoke)(
        {"base_url": state["base_url"]}
    )
    return {"reconnaissance": subgraph_output["reconnaissance"]}


# Planning Phase - create a test plan for the target website
def plan(state: State):
    subgraph_output = cached("plan", planning_graph.invoke)(
        {"base_url": state["base_url"], "reconnaissance": state["reconnaissance"]}
    )
    return {"plan": subgraph_output["plan"]}


def execute(state: State):
    index = state.get("plan_index", 0)
    subgraph_output = execution_graph.invoke(
        {
            "base_url": state["base_url"],
            "reconnaissance": state["reconnaissance"],
            "task": state["plan"][index],
        }
    )
    return {
        "plan_index": index + 1,
        "reports": state["reports"] + subgraph_output["reports"],
    }


def execution_routing(state: State):
    if state["plan_index"] < len(state["plan"]):
        return "execute"
    else:
        return END


llm = init_chat_model("anthropic:claude-sonnet-4-20250514", max_tokens=8192)

graph_builder = StateGraph(State)
graph_builder.add_node("reconnaissance", reconnoitre)
graph_builder.add_node("plan", plan)
graph_builder.add_node("execute", execute)

graph_builder.add_edge(START, "reconnaissance")
graph_builder.add_edge("reconnaissance", "plan")
graph_builder.add_edge("plan", "execute")
graph_builder.add_conditional_edges("execute", execution_routing)
graph_builder.add_edge("execute", END)

graph = graph_builder.compile()

# print(graph.get_graph(xray=1).draw_mermaid())

graph.invoke(
    {"base_url": "http://localhost:3000"},
    {"recursion_limit": 100, "callbacks": [ResponseCallback()]},
)
