from langchain_ollama import ChatOllama
from langchain.messages import HumanMessage, AIMessage
from utils.state import AgentState, OperationClassification,ItemDetails
from langgraph.types import Command
from utils.tools import show_items, add_item, update_item

tools_list = [show_items, add_item, update_item]
tools_by_name = {tool.name: tool for tool in tools_list}

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

    if operation['operation'] == "show_items":
        goto = "show_items"
    if operation['operation'] == "add_item":
        goto = "add_item"
    if operation['operation'] == "update_item":
        goto = "update_item"

    print(operation['operation'])
    return Command(
        update = {"operation" : operation},
        goto = goto
    )

#TODO: Show Items in the Database
def show_items(state: AgentState):
    """Shows the items in the database"""
    model_with_tool = llm.bind_tools(tools_list, tool_choice="add_item")
    result = model_with_tool.invoke(state['message_content'])
    tool_call = result.tool_calls[0]  # First (and only) tool call
    tool = tools_by_name[tool_call['name']]  # Lookup tool
    query = tool.invoke(tool_call['args'])  # Execute with args

    formatting_prompt = f"""
        You are a helpful assistant. Your job is to format dictionary into a table format for easier viewing.

        Given this message dictionary: {query}

        Format the dictionary to table
    """

    output = llm.invoke(formatting_prompt)

    print(output.content)

#TODO: Add Items to the Database
def add_item(state: AgentState):
    structured_llm = llm.with_structured_output(ItemDetails)
    classification_prompt = f"""
        You are a helpful assistant. Given a sentence you put items to a database by classifying different fields to each corresponding columns 

        Given this message: {state['message_content']}

        Categorize the different parts of the message such as the item_name, , description , and quantity.
    """
    classification = structured_llm.invoke(classification_prompt)
    print(classification)

    tool = tools_by_name["add_item"]
    result = tool.invoke({
        "item_name": classification.item_name,
        "description": classification.description, 
        "quantity": classification.quantity
    })
    
    return {
        "messages": [AIMessage(content=result)],  # Return success message
        "message_content": state['message_content']  # Preserve for state
    }

#TODO: Update Item Information in the Database
def update_item():
    print("TEST Classify Update Item")

#TODO: Generate the Notification of Changes to the User
def generate_update_notification():
    print("TEST Generate Update Notif")


#TODO: Send Update Message to the User
def send_update_message():
    print("TEST Send Update Message")