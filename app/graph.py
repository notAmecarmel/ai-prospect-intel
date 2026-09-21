from typing import Annotated, TypedDict

from langchain_core.messages import AnyMessage
from langgraph.graph.message import add_messages
from dotenv import load_dotenv
from langchain_google_genai import ChatGoogleGenerativeAI
from langgraph.graph import StateGraph, START, END
from langgraph.prebuilt import ToolNode
from app.schemas import CompanyAnalysis

from app.tools import get_company_information


# Load environment variables
load_dotenv()


# -----------------------------
# State
# -----------------------------
class AgentState(TypedDict):
    messages: Annotated[list[AnyMessage], add_messages]
    company_analysis: CompanyAnalysis | None
    pain_points: list[str]
    ai_opportunities: list[str]


# -----------------------------
# Tools
# -----------------------------

tools = [get_company_information]

tool_node = ToolNode(tools)


# -----------------------------
# LLM
# -----------------------------

llm = ChatGoogleGenerativeAI(
    model="gemini-3.8-flash"
)

llm_with_tools = llm.bind_tools(tools)

structured_llm = llm.with_structured_output(
    CompanyAnalysis
)


# -----------------------------
# Nodes
# -----------------------------

def agent_node(state: AgentState):
    response = llm_with_tools.invoke(
        state["messages"]
    )

    return {
        "messages": [response]
    }

def analysis_node(state: AgentState):
    tool_messages = [
        message
        for message in state["messages"]
        if message.type == "tool"
    ]

    company_information = tool_messages[-1].content

    result = structured_llm.invoke(
        [
            {
                "role": "user",
                "content": (
                    "Analyze the following company information "
                    "and identify the company's industry, target "
                    "customers, problems, and potential AI opportunities.\n\n"
                    f"Company information:\n{company_information}"
                ),
            }
        ]
    )

    return {
        "company_analysis": result
    }

def pain_point_node(state: AgentState):
    analysis = state["company_analysis"]

    result = llm.with_structured_output(
        list[str]
    ).invoke(
        [
            {
                "role": "user",
                "content": (
                    "Based on the following company analysis, "
                    "identify the most important operational or "
                    "business pain points this company is likely "
                    "to have.\n\n"
                    f"Company analysis:\n{analysis}"
                ),
            }
        ]
    )

    return {
        "pain_points": result
    }

def opportunity_node(state: AgentState):
    analysis = state["company_analysis"]
    pain_points = state["pain_points"]

    result = llm.with_structured_output(
        list[str]
    ).invoke(
        [
            {
                "role": "user",
                "content": (
                    "Identify practical AI opportunities for this "
                    "company based on its business analysis and "
                    "pain points.\n\n"
                    f"Company analysis:\n{analysis}\n\n"
                    f"Pain points:\n{pain_points}"
                ),
            }
        ]
    )

    return {
        "ai_opportunities": result
    }
# -----------------------------
# Routing
# -----------------------------

def should_continue(state: AgentState):

    last_message = state["messages"][-1]

    if last_message.tool_calls:
        return "tools"

    return "end"


# -----------------------------
# Graph
# -----------------------------

builder = StateGraph(AgentState)

builder.add_node("agent", agent_node)
builder.add_node("tools", tool_node)
builder.add_node("analysis", analysis_node)
builder.add_node("pain_points", pain_point_node)
builder.add_node("opportunities", opportunity_node)

builder.add_edge(START, "agent")

builder.add_conditional_edges(
    "agent",
    should_continue,
    {
        "tools": "tools",
        "end": "analysis",
    },
)

builder.add_edge("tools", "agent")
builder.add_edge("analysis", END)

graph = builder.compile()