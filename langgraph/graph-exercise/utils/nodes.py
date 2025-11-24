from langchain.messages import SystemMessage
from langchain.messages import ToolMessage
from langchain_core.messages import AIMessage
from langchain_ollama import ChatOllama
from tools import send_email, send_text_message

model = ChatOllama(
    model="qwen3:4b",
    temperature=0.7
)

tools_list = [send_email, send_text_message]
tools_by_name = {tool.name: tool for tool in tools_list}
model_with_tools = model.bind_tools(tools_list)

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
    return {"messages" : [AIMessage(content=message)]}
