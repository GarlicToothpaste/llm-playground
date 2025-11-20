from langchain_community.tools import DuckDuckGoSearchRun

search = DuckDuckGoSearchRun()

# print(search.invoke("What is indonesia?"))


from langchain_community.tools import DuckDuckGoSearchResults

search = DuckDuckGoSearchResults()

# print(search.invoke("What is indonesia?"))

search = DuckDuckGoSearchResults(output_format="list")

print(search.invoke("What is Indonesia?"))