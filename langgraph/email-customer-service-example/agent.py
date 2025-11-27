from utils.state import EmailAgentState, EmailClassification
from utils.nodes import read_email 
from langgraph.graph import StateGraph, START, END

workflow = StateGraph(EmailAgentState)

workflow.add_node("read_email", read_email)

workflow.add_edge(START, read_email)