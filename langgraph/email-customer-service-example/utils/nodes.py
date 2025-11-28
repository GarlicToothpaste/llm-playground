from langchain_ollama import ChatOllama
from langchain.messages import HumanMessage
from langgraph.types import interrupt, Command, RetryPolicy
from typing import Literal
from utils.state import EmailAgentState, EmailClassification

llm = ChatOllama(
    model="qwen3:4b",
    temperature=0.7
)

def read_email (state : EmailAgentState):
    """LLM Reads the Email Given by the User"""

    return {
        "messages": HumanMessage(content=f"Processing email: {state['email_content']}")
    }


# class EmailClassification(TypedDict):
#     intent: Literal["question", "bug", "billing", "feature", "complex"]
#     urgency: Literal["low", "medium", "high", "critical"]
#     topic : str 
#     summary : str 

def classify_intent(state : EmailAgentState) -> Command[Literal["search_documentation", "human_review", "draft_response", "bug_tracking"]]:
    """Use LLM to classify email intent and urgency, then route accordingly"""

    structured_llm = llm.with_structured_output(EmailClassification)

    classification_prompt = f"""
    Analyze this customer email and classify it:

    Email: {state['email_content']}
    From: {state['sender_email']}

    Provide classification including intent, urgency, topic, and summary.
    """

    classification = structured_llm.invoke(classification_prompt)

    if classification['intent'] == 'billing' or classification['urgency'] == 'critical':
        goto = "human_review"
    elif classification['intent'] in ['question', 'feature']:
        goto = "search_documentation"
    elif classification['intent'] == 'bug':
        goto = "bug_tracking"
    else:
        goto = "draft_response"

    return Command(
        update={"classification": classification},
        goto=goto
    )

def search_documentation(state : EmailAgentState) -> Command[Literal["draft_response"]]:
    """Searches knowledge base for information"""

    # Returns {} when there is no classification
    classification = state.get('classification' , {})
    query = f"{classification.get('intent', '')} {classification.get('topic', '')}"


def bug_tracking(state : EmailAgentState) -> Command[Literal["draft_response"]]:
    """Creates or update a bug report ticket"""

    ticket_id = "BUG-4245"
    return Command(
        update={
            "search_results" : [f"Bug Ticket with {ticket_id} created"],
            "current_step" : "bug_tracked"
        },
        goto = "draft_response"
    )