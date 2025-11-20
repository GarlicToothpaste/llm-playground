from smolagents import CodeAgent, LiteLLMModel

model = LiteLLMModel(
  model_id='ollama_chat/qwen3:4b'
) 

agent = CodeAgent(tools=[], model=model)

result = agent.run("Calculate the sum of numbers from 1 to 10")
print(result)