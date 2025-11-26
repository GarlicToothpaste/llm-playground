from langchain_ollama import ChatOllama
from langchain.messages import HumanMessage
from utils.state import EmailAgentState, EmailClassification

model = ChatOllama(
    model="qwen3:4b",
    temperature=0.7
)

def readHumanMessage (state : EmailAgentState):
    """LLM Reads the Email Given by the User"""

    return {
        "messages": HumanMessage(content=f"Processing email: {state['email_content']}")
    }