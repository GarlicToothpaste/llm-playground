import requests

class LocalEmbeddingFunction:
    def __init__(self, endpoint="http://localhost:1234/v1/embeddings"):
        self.endpoint = endpoint

    def embed_documents(self, texts):
        return [self.embed_query(text) for text in texts]

    def embed_query(self, text):
        response = requests.post(
            self.endpoint,
            json={"input": text, "model": "text-embedding-nomic-embed-text-v1.5"},
        )
        response.raise_for_status()
        return response.json()["data"][0]["embedding"]

def get_embedding_function():
    return LocalEmbeddingFunction()
