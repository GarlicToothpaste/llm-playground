import os
import asyncio
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.document_loaders import DirectoryLoader
from langchain_community.document_loaders import PyPDFLoader
from langchain_community.document_loaders import PyPDFDirectoryLoader
from langchain.schema.document import Document
from typing import List #For Python 3.8 and below
# from langchain.vectorstores.chroma import Chroma
from get_embedding_function import get_embedding_function


filename = 'company_rules.pdf'
dir_path = os.path.dirname(os.path.realpath(__file__))

directory_path = dir_path + '/data'

def load_documents():
    document_loader = PyPDFDirectoryLoader(directory_path)
    return document_loader.load()

def split_documents(documents: List[Document]):
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=800, 
        chunk_overlap=80,
        length_function=len,
        is_separator_regex=False
    )
    return text_splitter.split_documents(documents)

docs = load_documents()
