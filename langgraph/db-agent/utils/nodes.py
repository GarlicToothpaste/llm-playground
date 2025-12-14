from langchain_ollama import ChatOllama
from langchain.messages import HumanMessage
from utils.state import AgentState
llm = ChatOllama(
    model="qwen3:4b",
    temperature=0.7
)

def read_message(state: AgentState):
    print (state['message_content'])
    return {
        "messages": HumanMessage(content=f"Processing message: {state['message_content']}")
    }

#TODO: Classify Which Operation to use Based on the User Input
def classify_message():
    print("TEST Test Classify Message")

#TODO: Add Items to the Database
def add_item():
    print("TEST Classify Add_Item")

#TODO: Update Item Information in the Database
def update_item():
    print("TEST Classify Update Item")

#TODO: Generate the Notification of Changes to the User
def generate_update_notification():
    print("TEST Generate Update Notif")


#TODO: Send Update Message to the User
def send_update_message():
    print("TEST Send Update Message")