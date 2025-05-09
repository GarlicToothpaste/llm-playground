from langchain_tavily import TavilySearch
from pathlib import Path
from dotenv import load_dotenv

env_path = Path(__file__).parent / ".env"
load_dotenv(dotenv_path=env_path)  

tool = TavilySearch(max_results=2)
tools = [tool]
# item=tool.invoke("What's a 'node' in LangGraph?")
# print(item)
tool.invoke("What's a 'node' in LangGraph?")