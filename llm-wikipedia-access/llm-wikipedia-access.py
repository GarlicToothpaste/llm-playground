from langchain_community.retrievers import WikipediaRetriever
from langchain_core.prompts import PromptTemplate
from ollama import generate

def generate_query(query_txt:str):
    PROMPT_TEMPLATE = """
    You are an expert in Wikipedia. Your job is to help people find possible Wikpedia articles to answer their questions.

    ---

    Which topic in wikipedia can answer this question. Return only the search query and nothing else: {question}
    """

    prompt_template = PromptTemplate.from_template(PROMPT_TEMPLATE)
    prompt_template = prompt_template.format(question=query_txt)

    response = generate(model='qwen3:4b', prompt=prompt_template)

    return(response.response)

def search_wikipedia(query_txt:str):
    # Create the retriever
    wiki = WikipediaRetriever()

    # Query Wikipedia
    docs = wiki.invoke(query_txt)
        
    information = "\n---\n".join([f"**{doc.metadata['title']}**\n{doc.page_content}" for doc in docs])

    return information

def query_rag(query_txt:str):
    search_key = generate_query(query_txt)
    print(search_key)
    context_txt = search_wikipedia(search_key)
    print(context_txt)

    PROMPT_TEMPLATE = """
    You are an expert in summarizing Wikipedia articles. Your Job is helping people understand big wikipedia articles by summarizing them.
    Answer the question below given this article {context}

    ---

    Make a summary focusing around this question: {question}
    """

    prompt_template = PromptTemplate.from_template(PROMPT_TEMPLATE)
    prompt_template = prompt_template.format(context = context_txt ,question=query_txt)

    response = generate(model='qwen3:4b', prompt=prompt_template)

    return response

print(query_rag("Can you give me an overview of the film Inception?")['response'])