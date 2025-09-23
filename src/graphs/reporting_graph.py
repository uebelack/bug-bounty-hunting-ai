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


class ReportingState(MessagesState):
    result: str
    reports: List[Report]


def create_reporting_graph(llm: BaseChatModel):

    def create_report(state: ReportingState):
        structured_llm_with_tools = llm.with_structured_output(Reports)
        response = structured_llm_with_tools.invoke(
            state["messages"]
            + [
                HumanMessage(
                    content="Please create a structured report for each vulnerability."
                )
            ]
        )
        return {"reports": response.reports}

    graph_builder = StateGraph(ReportingState)
    graph_builder.add_node("create_report", create_report)
    graph_builder.add_edge(START, "create_report")
    graph_builder.add_edge("create_report", END)

    return graph_builder.compile()
