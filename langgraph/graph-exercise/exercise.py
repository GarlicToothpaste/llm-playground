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

from typing import Literal
from langgraph.graph import StateGraph, START, END


def should_continue(state: MessagesState) -> Literal["tool_node", END]:
    """Decide if we should continue the loop or stop based upon whether the LLM made a tool call"""

    messages = state["messages"]
    last_message = messages[-1]

    # If the LLM makes a tool call, then perform an action
    if last_message.tool_calls:
        return "tool_node"

    # Otherwise, we stop (reply to the user)
    return END