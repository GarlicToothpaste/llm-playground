from langchain.tools import tool
from langchain_community.retrievers import WikipediaRetriever
from langchain_community.tools import DuckDuckGoSearchRun

@tool
def search_wikipedia(word : str):
    """Searches Wikipedia given a string as a keyword"""
    wiki = WikipediaRetriever()
    docs = wiki.invoke(word)
    information = "\n---\n".join([f"**{doc.metadata['title']}**\n{doc.page_content}" for doc in docs])
    return information

@tool
def search_duckduckgo(word : str):
    """Searches the internet given a string as a keyword"""
    search = DuckDuckGoSearchRun()
    information = search.invoke(word)
    return information
