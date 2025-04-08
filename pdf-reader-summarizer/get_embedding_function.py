from langchain_community.embeddings.ollama import OllamaEmbeddings

def get_embedding_function():
    embeddings = OllamaEmbeddings(model="mlx-community/Llama-3.2-3B-Instruct-4bit")
    return embeddings