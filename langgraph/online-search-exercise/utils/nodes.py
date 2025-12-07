from utils.state import MessageState
from langchain_ollama import ChatOllama
from langchain.messages import HumanMessage
from utils.state import MessageClassification
from langgraph.types import Command

from utils.tools import search_wikipedia, search_duckduckgo

model = ChatOllama(
    model="qwen3:4b",
    temperature=0.7
)

tools_list = [search_wikipedia, search_duckduckgo]
tools_by_name = {tool.name: tool for tool in tools_list}
model_with_tools = model.bind_tools(tools_list)

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
    # print(classification)

    if classification['platform'] == "wikipedia":
        goto = "wikipedia_search"
    if classification['platform'] == "duckduckgo":
        goto = "duckduckgo_search"

    return Command(
        update = {"classification" : classification},
        goto = goto
    )

def duckduckgo_search(state: MessageState):

    prompt = f"""
        You are a helpful assistant. Your job is to provide a keyword based on a users message and use it to search on duckduckgo.

        Given this message {state['message_content']}

        Give a keyword to search.
    """
    print("DuckDuckGo Search")

    


def wikipedia_search(state: MessageState):
    
    prompt = f"""
        You are a helpful assistant. Your job is to provide a keyword based on a users message and use it to search on wikipedia.

        Given this message {state['message_content']}

        Give a keyword to search.
    """