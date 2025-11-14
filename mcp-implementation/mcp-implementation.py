from langchain_ollama import ChatOllama
# from langchain.agents import create_agent, tool

# Initialize the Ollama chat model
model = ChatOllama(
    model="qwen3:4b",  # or another model you've pulled (mistral, neural-chat, etc.)
    temperature=0.7
)

response = model.invoke("Hello")
print(response.content)