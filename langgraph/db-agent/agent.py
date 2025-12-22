from langgraph.graph import StateGraph, START, END
from utils.state import AgentState
from utils.nodes import read_message, classify_message, add_item, update_item, generate_update_notification, send_update_message, show_items

workflow = StateGraph(AgentState)

#Nodes
workflow.add_node("read_message", read_message)
workflow.add_node("classify_message", classify_message)
workflow.add_node("show_items", show_items)
workflow.add_node("add_item", add_item)
workflow.add_node("update_item", update_item)
workflow.add_node("generate_update_notification", generate_update_notification)
workflow.add_node("send_update_message", send_update_message)

#Edges
workflow.add_edge(START, "read_message")
workflow.add_edge("read_message", "classify_message")
# workflow.add_edge("classify_message", END)

app = workflow.compile()
initial_state = {
    # "message_content": "Show me all the items in the database." 
    "message_content": "Add an item with name of Paper, Description is A4 Size,  and Quantity of 100"
}

result = app.invoke(initial_state)