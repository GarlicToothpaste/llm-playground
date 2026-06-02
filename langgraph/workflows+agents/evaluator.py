#https://docs.langchain.com/oss/python/langgraph/workflows-agents

from langchain_ollama import ChatOllama

llm = ChatOllama(
    model="qwen3:4b",
    temperature=0.7
)

from typing import Annotated, List 
import operator
from typing_extensions import Literal , TypedDict
from pydantic import BaseModel, Field
from langchain_core.messages import HumanMessage, SystemMessage
from langgraph.graph import StateGraph, START, END

class State(TypedDict):
    joke: str
    topic: str
    feedback: str 
    funny_or_not: str

class Feedback(BaseModel):
    grade: Literal["funny", "not funny"] = Field(
        description="Decide if the joke is funny or not.",
    )
    feedback: str = Field(
        description="If the joke is not funny, provide feedback on how to improve it.",
    )

evaluator = llm.with_structured_output(Feedback)

def llm_call_generator(state: State):
    """LLM Generates a Joke"""
    if state.get("feedback"):
        msg = llm.invoke(
            f"Write a joke about {state['topic']} but take into account the feedback: {state['feedback']}"
        )

    else:
        msg = llm.invoke(f"Write a joke about {state['topic']}")
    return {"joke": msg.content}

def llm_call_evaluator(state: State):
    """LLM Evaluates the joke"""
    grade = evaluator.invoke(f"Grade the joke {state['joke']}")
    return {"funny_or_not" : grade.grade, "feedback": grade.feedback}

def route_joke(state: State):
    """Route back to joke generator or end based upon feedback from the evaluator"""
    if state['funny_or_not'] == "funny":
        return "Accepted"
    elif state["funny_or_not"] == "not funny":
        return "Rejected + Feedback"
    

optimizer_builder = StateGraph(State)

optimizer_builder.add_node("llm_call_generator", llm_call_generator)
optimizer_builder.add_node("llm_call_evaluator", llm_call_evaluator)

optimizer_builder.add_edge(START, "llm_call_generator")
optimizer_builder.add_edge("llm_call_generator", "llm_call_evaluator")
optimizer_builder.add_conditional_edges(
    "llm_call_evaluator",
    route_joke,
    {  
        "Accepted": END,
        "Rejected + Feedback": "llm_call_generator",
    },
)

optimizer_workflow = optimizer_builder.compile()

optimizer_workflow_graph = optimizer_workflow.get_graph().draw_mermaid_png()
with open("optimizer_builder.png", "wb") as f:
    f.write(optimizer_workflow_graph)

# Invoke
state = optimizer_workflow.invoke({"topic": "Cats"})
print(state["joke"])