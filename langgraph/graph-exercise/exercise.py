from langchain.messages import AnyMessage
from typing_extensions import TypedDict, Annotated
import operator
from typing import Literal
from langgraph.graph import StateGraph, START, END

class MessagesState(TypedDict):
    messages: Annotated[list[AnyMessage], operator.add]
    llm_calls: int


def should_continue(state: MessagesState) -> Literal["tool_node", "end_message_node"]:
    """Decide if we should continue the loop or stop based upon whether the LLM made a tool call"""

    messages = state["messages"]
    last_message = messages[-1]

    # If the LLM makes a tool call, then perform an action
    if last_message.tool_calls:
        return "tool_node"

    # Otherwise, we stop (reply to the user)
    return "end_message_node"

from nodes import llm_call
from nodes import tool_node
from nodes import end_message_node

# Build workflow
agent_builder = StateGraph(MessagesState)

# Add nodes
agent_builder.add_node("llm_call", llm_call)
agent_builder.add_node("tool_node", tool_node)
agent_builder.add_node("end_message_node", end_message_node)

# Add edges to connect nodes
agent_builder.add_edge(START, "llm_call")
agent_builder.add_conditional_edges(
    "llm_call",
    should_continue,
    ["tool_node", "end_message_node"]
)
agent_builder.add_edge("tool_node", "llm_call")
agent_builder.add_edge("end_message_node" , END)
# Compile the agent
agent = agent_builder.compile()

# Invoke
# from langchain.messages import HumanMessage
# messages = [HumanMessage(content="Add 3 and 4.")]
# messages = agent.invoke({"messages": messages})
# for m in messages["messages"]:
#     m.pretty_print()


from langchain.messages import HumanMessage
messages = [HumanMessage(content="Send an email to bob.green@gmail.com")]
messages = agent.invoke({"messages": messages})
for m in messages["messages"]:
    m.pretty_print()