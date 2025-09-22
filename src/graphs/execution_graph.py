from planning_graph import PlanItem


def execute_plan_item(state: State):
    print(f"🛠️ Executing plan item {state['plan_item_index']} ...")
    print(f"🛠️ Plan: {state['plan'].items}")
    plan_item = state["plan"].items[state["plan_item_index"]]
    print(f"🛠️ Plan item: {plan_item.title}")
    print(f"🛠️ Plan item prompt: {plan_item.prompt}")

    response = llm.invoke(
        [
            SystemMessage(content=plan_item.prompt),
            HumanMessage(
                content=f"The target website is {state['base_url']}. The plan item is {plan_item.title}."
            ),
        ]
    )
    return {"plan_item": response, "plan_item_index": state["plan_item_index"] + 1}


from langchain_core.messages import SystemMessage, HumanMessage
from langchain.chat_models import init_chat_model
from langgraph.graph import StateGraph, START, END
from typing import List, TypedDict
from pydantic import BaseModel, Field

llm = init_chat_model("anthropic:claude-sonnet-4-20250514", max_tokens=8192)


class State(TypedDict):
    base_url: str
    reconnaissance: str
    plan: List[PlanItem]


def plan(state: State):
    print(f"🛠️ Planning ...")
    response = llm.with_structured_output(Plan).invoke(
        [
            SystemMessage(
                content=(
                    "You are a planning assistant for a bug-bounty engagement. "
                    "Using the provided recon outputs, produce a compact, topic-focused test plan that assigns different testers to cover specific vulnerability categories (OWASP Top 10 + API, business logic, misconfigurations, supply-chain). "
                    "Requirements: 1) Confirm written authorization and scope before any active/authenticated steps; if none, produce passive-only plans. "
                    "2) Do NOT include exploit steps, payloads, or bypass techniques — only high-level scenarios and remediation. "
                    "Deliverables (concise): for each topic produce a scenario ID, objective, allowed technique level (passive | authorized active | authenticated), preconditions, success/detection criteria, evidence to collect, remediation notes, and priority. "
                    "Tone: precise, risk-aware, and machine-readable where possible."
                )
            ),
            HumanMessage(content=f"The target website is {state['base_url']}."),
        ]
    )

    return {"plan": response.items}


graph_builder = StateGraph(State)
graph_builder.add_node("plan", plan)

graph_builder.add_edge(START, "plan")
graph_builder.add_edge("plan", END)

planning_graph = graph_builder.compile()
