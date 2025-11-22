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
