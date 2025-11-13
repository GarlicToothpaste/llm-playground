from langchain_community.retrievers import WikipediaRetriever
from langchain_core.prompts import PromptTemplate
from ollama import generate

# # Create the retriever
# wiki = WikipediaRetriever()

# # Query Wikipedia
# docs = wiki.invoke("Orb: On the Movements of the Earth")

# print(docs)


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


print(query_rag("Who is the director of the movie Inception"))
