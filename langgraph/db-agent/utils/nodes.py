from langchain_ollama import ChatOllama

llm = ChatOllama(
    model="qwen3:4b",
    temperature=0.7
)

#TODO: Read User Input
def read_message():
    print("TEST Read Message")

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