
from langchain.chat_models import ChatOpenAI
from langchain.schema import HumanMessage

llm = ChatOpenAI(
    model="llama-3.2-3b-instruct",
    base_url="http://127.0.0.1:1234/v1",
    api_key="any"
)
text = "Test Message?"
response = llm.invoke([HumanMessage(content=text)])
print(response.content)