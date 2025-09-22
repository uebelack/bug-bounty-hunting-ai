from langchain_core.messages import SystemMessage, HumanMessage
from langchain_core.language_models.chat_models import BaseChatModel
from langgraph.graph import StateGraph, START, END
from typing import List, TypedDict
from pydantic import BaseModel, Field


class Task(BaseModel):
    title: str = Field(
        description="Descriptive title for this specific security assessment task \
            (e.g., 'Directory Enumeration', 'Authentication Testing', 'Input Validation Analysis')",
    )
    instructions: str = Field(
        description="Detailed instructions that guides the bug bounty hunter agent \
            on how to execute this specific task, including objectives, methodologies, \
            tools to use, success criteria, and expected deliverables",
    )


class Plan(BaseModel):
    tasks: List[Task] = Field(
        description="List of tasks to be executed during the bug bounty engagement",
    )


class State(TypedDict):
    base_url: str
    reconnaissance: str
    plan: List[Task]


SYSTEM_PROMPT = """
You are a planning assistant for a bug-bounty engagement.
Using the provided recon outputs, produce a compact, topic-focused test plan that assigns 
different testers to cover specific vulnerability categories (OWASP Top 10 + API, business logic, 
misconfigurations, supply-chain).
"""


def create_planning_graph(llm: BaseChatModel):
    def plan(state: State):
        print(f"🛠️ Planning ...")
        response = llm.with_structured_output(Plan).invoke(
            [
                SystemMessage(content=(SYSTEM_PROMPT)),
                HumanMessage(content=f"The target website is {state['base_url']}."),
            ]
        )

        return {"plan": response.tasks}

    graph_builder = StateGraph(State)
    graph_builder.add_node("plan", plan)

    graph_builder.add_edge(START, "plan")
    graph_builder.add_edge("plan", END)

    return graph_builder.compile()
