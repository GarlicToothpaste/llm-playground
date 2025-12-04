from langgraph.graph import StateGraph, START, END
from utils.state import MessageState
from utils.nodes import read_message

workflow = StateGraph(MessageState)

workflow.add_node("read_message", read_message)
workflow.add_edge(START, "read_message")
workflow.add_edge("read_message", END)

app = workflow.compile()

# initial_state = {
#     "email_content": "I was charged twice for my subscription! This is urgent!",
#     "sender_email": "customer@example.com",
#     "email_id": "email_123",
#     "messages": []
# }

# result = app.invoke(initial_state, config)
