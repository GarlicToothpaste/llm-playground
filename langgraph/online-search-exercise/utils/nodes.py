from utils.state import MessageState
from langchain_ollama import ChatOllama
from langchain.messages import HumanMessage

llm = ChatOllama(
    model="qwen3:4b",
    temperature=0.7
)

def read_message(state:MessageState):
    """LLM Reads the User Message"""
    print("Test Node")
    return {
        "messages": HumanMessage(content=f"Processing message: {state['message_content']}")
    }



def classify_message(state:MessageState):
    print("Placeholder")