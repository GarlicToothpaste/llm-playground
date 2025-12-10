from langgraph.graph import StateGraph, START, END
from utils.state import MessageState
from utils.nodes import read_message, classify_message, duckduckgo_search, wikipedia_search, summarize_search, send_reply

workflow = StateGraph(MessageState)

#Nodes
workflow.add_node("read_message", read_message)
workflow.add_node("classify_message", classify_message)
workflow.add_node("duckduckgo_search", duckduckgo_search)
workflow.add_node("wikipedia_search", wikipedia_search)
workflow.add_node("summarize_search", summarize_search)
workflow.add_node("send_reply", send_reply)

#Edges
workflow.add_edge(START, "read_message")
workflow.add_edge("read_message", "classify_message")
workflow.add_edge("send_reply", END)
# workflow.add_edge("read_message", END)


app = workflow.compile()

initial_state = {
    "message_content": "Use wikipedia to search about Pope Urban II"
}

result = app.invoke(initial_state)

