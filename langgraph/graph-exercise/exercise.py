from typing import Literal
from langgraph.graph import StateGraph, START, END
from utils.state import MessagesState
from langchain.messages import HumanMessage
from utils.nodes import llm_call, tool_node, end_message_node

def should_continue(state: MessagesState) -> Literal["tool_node", "end_message_node"]:
    """Decide if we should continue the loop or stop based upon whether the LLM made a tool call"""

    messages = state["messages"]
    last_message = messages[-1]

    # If the LLM makes a tool call, then perform an action
    if last_message.tool_calls:
        return "tool_node"

    # Otherwise, we stop (reply to the user)
    return "end_message_node"

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


messages = [HumanMessage(content="Send an email to bob.green@gmail.com and send a text message to 09207801532")]
messages = agent.invoke({"messages": messages})
for m in messages["messages"]:
    m.pretty_print()