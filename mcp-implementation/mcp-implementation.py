from langchain_ollama import ChatOllama
from langchain.agents import create_agent
from langchain.tools import tool
# Initialize the Ollama chat model
model = ChatOllama(
    model="qwen3:4b",  # or another model you've pulled (mistral, neural-chat, etc.)
    temperature=0.7
)
# response = model.invoke("Hello")
# print(response.content)

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
 
agent = create_agent(
    model = model,
    tools = [add_numbers , multiply_numbers, get_system_time],
    system_prompt= "You are a helpful assistant, use tools when needed."
)

result = agent.invoke({
    "messages": [{"role": "user", "content": "What's 5 plus 3 and what is the current system time?"}]
})

print(result)