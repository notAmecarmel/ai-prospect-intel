from typing import Annotated, TypedDict

from langchain_core.messages import AnyMessage
from langgraph.graph.message import add_messages
from dotenv import load_dotenv
from langchain_google_genai import ChatGoogleGenerativeAI
from langgraph.graph import StateGraph, START, END
from langgraph.prebuilt import ToolNode

from app.tools import get_company_information


# Load environment variables
load_dotenv()


# -----------------------------
# State
# -----------------------------
class AgentState(TypedDict):
    messages: Annotated[list[AnyMessage], add_messages]


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

builder.add_edge(START, "agent")

builder.add_conditional_edges(
    "agent",
    should_continue,
    {
        "tools": "tools",
        "end": END,
    },
)

builder.add_edge("tools", "agent")

graph = builder.compile()