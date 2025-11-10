# from langchain_ollama import OllamaEmbeddings

# def get_embedding_function():
#     embeddings = OllamaEmbeddings(model="nomic-embed-text")
#     return embeddings


from langchain_ollama.embeddings import OllamaEmbeddings

# Initialize OllamaEmbeddings with the Nomic model
embeddings = OllamaEmbeddings(model="embeddinggemma")

print("TEST")
# Example: Generate embeddings for a document
document_embeddings = embeddings.embed_documents(
    [
        "This is a document about machine learning.",
        "Another document discussing natural language processing.",
    ]
)

# Example: Generate an embedding for a query

query_embedding = embeddings.embed_query("What is AI?")
print("Document Embeddings:", document_embeddings)
print("Query Embedding:", query_embedding)

# curl http://127.0.0.1:11434/api/embeddings \
#   -H "Content-Type: application/json" \
#   -d '{"model":"nomic-embed-text","prompt":"hello there who are you"}'