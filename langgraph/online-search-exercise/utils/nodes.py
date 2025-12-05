from utils.state import MessageState
from langchain_ollama import ChatOllama
from langchain.messages import HumanMessage
from utils.state import MessageClassification

llm = ChatOllama(
    model="qwen3:4b",
    temperature=0.7
)

def read_message(state:MessageState):
    """LLM Reads the User Message"""
    print("Test Node")
    return {
        "messages": HumanMessage(content=f"Processing message: {state['message_content']}")
    }

def classify_message(state:MessageState):
    """Use LLM to classify wether to use wikipedia or duckduckgo search"""

    structured_llm = llm.with_structured_output(MessageClassification)

    classification_prompt = f"""
    Analyze this message and classify which website we will use for searching

    Message: {state['message_content']}

    Provide classification on which tool to use.
    """

    classification = structured_llm.invoke(classification_prompt)
    print(classification)