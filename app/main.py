from langchain_core.messages import HumanMessage

from app.graph import graph


result = graph.invoke(
    {
        "messages": [
            HumanMessage(
                content="Research Acme Manufacturing and tell me what the company does."
            )
        ]
    }
)


for message in result["messages"]:
    print("\n---")
    print(type(message).__name__)

    if message.content:
        print(message.content)

    if hasattr(message, "tool_calls") and message.tool_calls:
        print("TOOL CALLS:")
        print(message.tool_calls)