from langchain_core.messages import SystemMessage, HumanMessage
from langchain.chat_models import init_chat_model
from langgraph.graph import StateGraph, START, END
from typing import List, TypedDict
from pydantic import BaseModel, Field

llm = init_chat_model("anthropic:claude-sonnet-4-20250514", max_tokens=8192)


class PlanItem(BaseModel):
    title: str = Field(
        description="Descriptive title for this specific testing phase or security assessment task (e.g., 'Directory Enumeration', 'Authentication Testing', 'Input Validation Analysis')",
    )
    prompt: str = Field(
        description="Detailed instruction prompt that guides the agent on how to execute this specific testing phase, including objectives, methodologies, tools to use, success criteria, and expected deliverables",
    )


class Plan(BaseModel):
    items: List[PlanItem] = Field(
        description="Ordered sequence of security testing phases and assessment tasks to be executed during the bug bounty engagement, prioritized by risk level and logical testing progression (reconnaissance → enumeration → vulnerability assessment → exploitation → post-exploitation)",
    )


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
