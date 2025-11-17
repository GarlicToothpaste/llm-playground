from langchain_ollama import ChatOllama
from langchain.agents import create_agent
from langchain.agents.middleware import PIIMiddleware

model = ChatOllama(
    model="qwen3:4b",
    temperature=0.7
)

agent = create_agent(
    model=model,
    middleware= [
        PIIMiddleware(
            "email",
            strategy="redact",
            apply_to_input=True
        ),
    ]
)

result = agent.invoke({
    "messages": [{"role": "user", "content": "My email is john.doe@example.com what is my email?"}]
})
print(result)