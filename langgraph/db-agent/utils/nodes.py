from langchain_ollama import ChatOllama
from langchain.messages import HumanMessage
from utils.state import AgentState, OperationClassification
from langgraph.types import Command

llm = ChatOllama(
    model="qwen3:4b",
    temperature=0.7
)

def read_message(state: AgentState):
    """Reads the message input of the user"""
    return {
        "messages": HumanMessage(content=f"Processing message: {state['message_content']}")
    }

#TODO: Classify Which Operation to use Based on the User Input
def classify_message(state: AgentState):
    """Use the LLM to classify which tool to use"""

    structured_llm = llm.with_structured_output(OperationClassification)

    classification_prompt = f"""
    Analyze this message and classify which sql function it will use

    Message: {state['message_content']}

    Classify the sql function
    """

    operation = structured_llm.invoke(classification_prompt)
    # print(classification)

    if classification['operation'] == "add_item":
        goto = "add_item"
    if classification['operation'] == "update_item":
        goto = "update_item"

    print(classification['operation'])
    return Command(
        update = {"classification" : classification},
        goto = goto
    )

#TODO: Add Items to the Database
def add_item(state: AgentState):
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