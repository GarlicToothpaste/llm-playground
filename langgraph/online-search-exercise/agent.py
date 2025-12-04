from langgraph.graph import StateGraph, START, END
from utils.state import MessageState
from utils.nodes import read_message

workflow = StateGraph(MessageState)

workflow.add_node("read_message", read_message)
workflow.add_edge(START, "read_message")
workflow.add_edge("read_message", END)

app = workflow.compile()

initial_state = {
    "message_content": "This is a test message"
    # "sender_email": "customer@example.com",
    # "email_id": "email_123",
    # "messages": []
}

result = app.invoke(initial_state)
