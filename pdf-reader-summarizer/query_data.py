import os 
from get_embedding_function import get_embedding_function
from langchain_chroma import Chroma

dir_path = os.path.dirname(os.path.realpath(__file__))
chroma_path = dir_path + '/chroma'

PROMPT_TEMPLATE = """
Answer the question based only on the following:

{context}

---

Answer the question based on the above context: {question}
"""

def query_rag(query_txt:str):
    db = Chroma(
        persist_directory=chroma_path,
        embedding_function=get_embedding_function()
    ) 

    results = db.similarity_search(query_txt, k=5)
    print(results)

query_rag("What are the rules of a speed die")

#TODO Perpare the template

#TODO Feed it to the llm