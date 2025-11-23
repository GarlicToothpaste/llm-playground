from langchain.tools import tool
from langchain_ollama import ChatOllama


model = ChatOllama(
    model="qwen3:4b",
    temperature=0.7
)

@tool
def send_email(email: str ) -> str:
    """Given an email address, send an email.
    
    Args :
        email: Email Address of the User
    """

    status = "Email sent!"
    return status

@tool
def send_text_message(mobile_number: str) -> str:
    """Given a mobile number, send a text message

    Args:
        a: mobile number of the recipient
    """
    return mobile_number

tools = [send_email, send_text_message]
tools_by_name = {tool.name: tool for tool in tools}
model_with_tools = model.bind_tools(tools)


from langchain.messages import AnyMessage
from typing_extensions import TypedDict, Annotated
import operator


class MessagesState(TypedDict):
    messages: Annotated[list[AnyMessage], operator.add]
    llm_calls: int

from langchain.messages import SystemMessage


def llm_call(state: dict):
    """LLM decides whether to call a tool or not"""

    return {
        "messages": [
            model_with_tools.invoke(
                [
                    SystemMessage(
                        content="You are an assistant that helps contact people given contact details"
                    )
                ]
                + state["messages"]
            )
        ],
        "llm_calls": state.get('llm_calls', 0) + 1
    }

from langchain.messages import ToolMessage

## Calls the Tools and Invokes all
def tool_node(state: dict):
    """Performs the tool call"""

    result = []
    for tool_call in state["messages"][-1].tool_calls:
        tool = tools_by_name[tool_call["name"]]
        observation = tool.invoke(tool_call["args"])
        result.append(ToolMessage(content=observation, tool_call_id=tool_call["id"]))
    return {"messages": result}

def end_message_node(state: dict):
    """Thanks the user after using the application"""
    message = "Thank you for using this AI. We hope we have helped you!"
    return {"messages" : message}

from typing import Literal
from langgraph.graph import StateGraph, START, END


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

# Show the agent
# from IPython.display import Image, display
# display(Image(agent.get_graph(xray=True).draw_mermaid_png()))

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