import os
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.document_loaders import PyPDFDirectoryLoader
from langchain.schema.document import Document
from langchain_chroma import Chroma
import get_embedding_function

dir_path = os.path.dirname(os.path.realpath(__file__))
directory_path = dir_path + '/data'
chroma_path = dir_path + '/chroma'

def main():
    docs = load_documents()
    chunks= split_documents(docs)
    add_to_chromadb(chunks)

def load_documents():
    document_loader = PyPDFDirectoryLoader(directory_path)
    return document_loader.load()

def split_documents(documents: list[Document]):
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=800, 
        chunk_overlap=80,
        length_function=len,
        is_separator_regex=False
    )
    return text_splitter.split_documents(documents)

def calculate_chunk_ids(chunks):
    last_page_id = None
    current_chunk_index = 0
    for chunk in chunks:
        source = chunk.metadata.get("source")
        page = chunk.metadata.get("page")
        current_page_id = f"{source}:{page}"

        if current_page_id == last_page_id:
            current_chunk_index+=1 
        else:
            current_chunk_index=0

        chunk_id= f"{current_page_id}:{current_chunk_index}"
        last_page_id=current_page_id
        
        chunk.metadata['id']=chunk_id
    return chunks

def add_to_chromadb(chunks):
    db = Chroma(
        persist_directory=chroma_path,
        embedding_function=get_embedding_function.get_embedding_function()
    )

    chunks_with_ids = calculate_chunk_ids(chunks)

    existing_items = db.get()
    existing_ids = set(existing_items["ids"])
    print(f"Existing docs in DB: {len(existing_ids)}")

    new_chunks = []
    for chunk in chunks_with_ids:
        if chunk.metadata["id"] not in existing_ids:
            new_chunks.append(chunk)

    if len(new_chunks):
        print(f"Adding new documents: {len(new_chunks)}")
        new_chunk_ids = [chunk.metadata["id"] for chunk in new_chunks]
        db.add_documents(new_chunks, ids=new_chunk_ids)
        
    else:
        print("No new documents to add")

if __name__ == "__main__":
    main()