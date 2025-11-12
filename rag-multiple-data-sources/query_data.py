import os 
from get_embedding_function import get_embedding_function
from langchain_chroma import Chroma
from langchain_core.prompts import PromptTemplate
from pprint import pprint
from ollama import generate

dir_path = os.path.dirname(os.path.realpath(__file__))
chroma_path = dir_path + '/chroma'

PROMPT_TEMPLATE = """
Answer the question based only on the following:
{context}

---

Answer the question based on the above data: {question}
"""

def query_rag(query_txt:str):
    db = Chroma(
        persist_directory=chroma_path,
        embedding_function=get_embedding_function()
    ) 

    results = db.similarity_search(query_txt, k=5)
    # pprint(results[0].page_content)
    context_text = "\n\n---\n\n".join([doc.page_content for doc in results])
    # print(context_text)

    prompt_template = PromptTemplate.from_template(PROMPT_TEMPLATE)
    prompt_template = prompt_template.format(context=context_text, question=query_txt)

    response = generate(model='qwen3:4b', prompt=prompt_template)

    return(response.response)
query_rag("How much total money does a player start with in Monopoly? (Answer with the number only)")