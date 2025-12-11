from utils.state import MessageState
from langchain_ollama import ChatOllama
from langchain.messages import HumanMessage, AIMessage
from utils.state import MessageClassification
from langgraph.types import Command

from utils.tools import search_wikipedia, search_duckduckgo

llm = ChatOllama(
    model="qwen3:4b",
    temperature=0.7
)

tools_list = [search_wikipedia, search_duckduckgo]
tools_by_name = {tool.name: tool for tool in tools_list}
# model_with_tools = llm.bind_tools(tools_list)

def read_message(state:MessageState):
    """LLM Reads the User Message"""
    # print("Test Node")
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

    keyword_prompt = f"""
        You are a helpful assistant. Your job is to provide a keyword based on a users message and use it to search on duckduckgo.

        Given this message {state['message_content']}

        Give a keyword to search.
    """
    keyword = llm.invoke(keyword_prompt)
    model_with_duckduckgo = llm.bind_tools(tools_list, tool_choice="search_duckduckgo")

    result = model_with_duckduckgo.invoke(f"Search wikipedia for this keyword: {keyword}")
    tool_call = result.tool_calls[0]  # First (and only) tool call
    tool = tools_by_name[tool_call['name']]  # Lookup tool
    search_result = tool.invoke(tool_call['args'])  # Execute with args
    
    # print(f"Tool result: {search_result}")    

    return Command(
        update = {"search_result" : search_result},
        goto = "summarize_search"
    )

def wikipedia_search(state: MessageState):
    
    keyword_prompt = f"""
        You are a helpful assistant. Your job is to provide a keyword based on a users message and use it to search on wikipedia.

        Given this message {state['message_content']}

        Give a keyword to search.
    """
    keyword = llm.invoke(keyword_prompt)
    # print (keyword)
    model_with_wikipedia = llm.bind_tools(tools_list, tool_choice="search_wikipedia")

    result = model_with_wikipedia.invoke(f"Search wikipedia for this keyword: {keyword}")
    tool_call = result.tool_calls[0]  # First (and only) tool call
    tool = tools_by_name[tool_call['name']]  # Lookup tool
    tool_result = tool.invoke(tool_call['args'])  # Execute with args
    
    search_result = tool.invoke(tool_call['args'])  # Execute with args
    
    # print(f"Tool result: {search_result}")    

    return Command(
        update = {"search_result" : search_result},
        goto = "summarize_search"
    )

def summarize_search(state: MessageState):
    # message = state.get("search_result")

    keyword_prompt = f"""
        You are a helpful assistant. Your job is to summarize items searched on the internet.

        Given this search result {state['search_result']}

        Summarize the data to help the user understand the important parts
    """

    search_summary = llm.invoke(keyword_prompt)

    # print(search_summary)

    return Command(
        update = {"search_summary": search_summary},
        goto = "send_reply"
    )

def send_reply(state: MessageState):
    # print("Sample Reply")
    message = state['search_summary'].content
    return {"messages" : [AIMessage(content=message)]}