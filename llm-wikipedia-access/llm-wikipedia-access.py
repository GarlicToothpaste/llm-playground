from langchain_community.retrievers import WikipediaRetriever

# Create the retriever
wiki = WikipediaRetriever()

# Query Wikipedia
docs = wiki.invoke("Orb: On the Movements of the Earth")

print(docs)