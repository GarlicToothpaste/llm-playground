from langchain_community.document_loaders import PyPDFLoader
import os
import asyncio

filename = 'company_rules.pdf'
dir_path = os.path.dirname(os.path.realpath(__file__))

pdf_file_path = dir_path + '/' + filename

async def load_pages():
    loader = PyPDFLoader(pdf_file_path)
    pages = []
    async for page in loader.alazy_load():
        pages.append(page)
    return pages

if __name__ == "__main__":
    pages = asyncio.run(load_pages())
    print(pdf_file_path)
    print(pages)