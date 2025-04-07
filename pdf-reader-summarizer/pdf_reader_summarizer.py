from langchain_community.document_loaders import PyPDFLoader
import os
import asyncio
from langchain.chat_models import ChatOpenAI
from langchain.schema import HumanMessage

filename = 'company_rules.pdf'
dir_path = os.path.dirname(os.path.realpath(__file__))

pdf_file_path = dir_path + '/' + filename

async def load_pages():
    loader = PyPDFLoader(pdf_file_path)
    pages = []
    async for page in loader.alazy_load():
        # pages.append(page.page_content)
        pages.append(page)
    
    # pages = " ".join(pages)
    return pages

if __name__ == "__main__":
    pages = asyncio.run(load_pages())
    # print(pdf_file_path)
    # print(type(pages))
    # print(pages[2])

llm = ChatOpenAI(
    model_name="llama-3.2-3b-instruct",  # Can be anything; LM Studio ignores it
    openai_api_base="http://localhost:1234/v1",  # LM Studio's endpoint
    openai_api_key="not-needed",  # Required by LangChain, but ignored by LM Studio
)

text = "Given the contents of this pdf file. What is the vision of the company?\n" +  pages[2].page_content
response = llm([HumanMessage(content=text)])
print(response.content)