import os 
dir_path = os.path.dirname(os.path.realpath(__file__))
chroma_path = dir_path + '/chroma'
from langchain_chroma import Chroma
from get_embedding_function import get_embedding_function
from langchain_core.prompts import PromptTemplate
from ollama import generate

QUESTION_TEMPLATE = """
This is the context:
{context}


---

Answer this question using the above data:
{question}

"""


def query_data(query_text : str):
    db = Chroma(persist_directory=chroma_path,embedding_function=get_embedding_function())    
    context = db.similarity_search(query_text , k=5)       
    context = "\n\n---\n\n".join(doc.page_content for doc in context)
    prompt = PromptTemplate.from_template(QUESTION_TEMPLATE)
    # prompt = prompt.invoke({"context":context, "question":query_text})
    prompt = prompt.template.format(context=context, question=query_text)
    
    response = generate(model="mistral-small:24b", prompt=prompt)
    print(response.response)



query_data("What are other InuYasha shows in netflix?")