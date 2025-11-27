from langchain_ollama import ChatOllama
from langchain.messages import HumanMessage
from langgraph.types import interrupt, Command, RetryPolicy
from typing import Literal
from utils.state import EmailAgentState, EmailClassification

model = ChatOllama(
    model="qwen3:4b",
    temperature=0.7
)

def read_email (state : EmailAgentState):
    """LLM Reads the Email Given by the User"""

    return {
        "messages": HumanMessage(content=f"Processing email: {state['email_content']}")
    }

def classify_intent(state : EmailAgentState):
    "To Do"