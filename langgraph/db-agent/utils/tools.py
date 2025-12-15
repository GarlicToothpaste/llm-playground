from langchain.tools import tool
from langchain_community.utilities import SQLDatabase

db = SQLDatabase.from_uri("jdbc:mysql://localhost:3306/?user=root")
#TODO: Show Database Contents
@tool
def show_items():
    print("Test")

#TODO: Adds the Item Name, Description, and Available Stock to the DB
@tool
def add_item():
    print("Test")

#TODO: Updates the Item Name, Description, and Available Stock to the DB
@tool
def update_item():
    print("Test")