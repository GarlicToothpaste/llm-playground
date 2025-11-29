from utils.state import EmailAgentState, EmailClassification
from utils.nodes import read_email , classify_intent,bug_tracking
from langgraph.graph import StateGraph, START, END

workflow = StateGraph(EmailAgentState)

workflow.add_node("read_email", read_email)
workflow.add_node("classify_intent", classify_intent)

workflow.add_edge(START, "read_email")
workflow.add_edge("read_email", "classify_intent")


workflow.add_node("bug_tracking", bug_tracking)