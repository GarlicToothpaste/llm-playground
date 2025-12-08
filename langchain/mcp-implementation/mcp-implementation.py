from langchain_ollama import ChatOllama
from langchain.agents import create_agent
from langchain.tools import tool
from langchain_community.retrievers import WikipediaRetriever
from langchain_community.tools import DuckDuckGoSearchRun

# Initialize the Ollama chat model
model = ChatOllama(
    model="qwen3:4b",  # or another model you've pulled (mistral, neural-chat, etc.)
    temperature=0.7
)
# response = model.invoke("Hello")
# print(response.content)

#TODO: Add a functionality that uses an API
@tool
def add_numbers (a : int , b : int):
    """Adds two numbers together"""
    return a + b 

@tool
def multiply_numbers (a:int , b:int):
    """Multiplies two numbers together"""
    return a * b 

@tool
def get_system_time():
    """Gets the system time"""
    time = "It is 12:00"
    return time

@tool
def search_wikipedia(word : str):
    """Searches Wikipedia given a string as a keyword"""
    wiki = WikipediaRetriever()
    docs = wiki.invoke(word)
    information = "\n---\n".join([f"**{doc.metadata['title']}**\n{doc.page_content}" for doc in docs])
    return information

@tool
def search_internet(word : str):
    """Searches the internet given a string as a keyword"""
    search = DuckDuckGoSearchRun()
    information = search.invoke(word)
    return information

agent = create_agent(
    model = model,
    tools = [add_numbers , multiply_numbers, get_system_time, search_wikipedia , search_internet],
    system_prompt= "You are a helpful assistant, use tools when needed."
)

result = agent.invoke({
    "messages": [{"role": "user", "content": "Can you search the wikipedia about Indonesia? What does it say about it?"}]
})

# print(result["messages"][-1].content)
print (result)