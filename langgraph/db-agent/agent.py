from langgraph.graph import StateGraph, START, END
from utils.state import AgentState
from utils.nodes import read_message, classify_message, add_item, update_item, generate_update_notification, send_update_message

workflow = StateGraph(AgentState)

#Nodes
workflow.add_node("read_message", read_message)
workflow.add_node("classify_message", classify_message)
workflow.add_node("add_item", add_item)
workflow.add_node("update_item", update_item)
workflow.add_node("generate_update_notification", generate_update_notification)
workflow.add_node("send_update_message", send_update_message)

#Edges
workflow.add_edge(START, "read_message")
workflow.add_edge("read_message", END)

app = workflow.compile()
initial_state = {
    "message_content": "Test Message"
}

result = app.invoke(initial_state)