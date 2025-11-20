import os 
from langchain_community.document_loaders import DirectoryLoader
from langchain_community.document_loaders.csv_loader import CSVLoader
from langchain_community.document_loaders import PyPDFLoader
from langchain_community.document_loaders.merge import MergedDataLoader
from langchain_community.document_loaders import PyPDFDirectoryLoader

# from pprint import pprint
import re
from get_embedding_function import get_embedding_function
from langchain_chroma import Chroma
import chromadb

dir_path = os.path.dirname(os.path.realpath(__file__))
directory_path = dir_path + '/data'
chroma_path = dir_path + '/chroma'

def main():
    data = load_documents()
    add_to_chroma_db(data)
    
def load_documents():
    csv_loader = DirectoryLoader(directory_path, glob='**/*.csv', loader_cls=CSVLoader)
    pdf_loader = DirectoryLoader(directory_path, glob='**/*.pdf', loader_cls=PyPDFLoader)
    merged_loader = MergedDataLoader(loaders=[csv_loader, pdf_loader])
    data =merged_loader.load()
    return data

def calculate_chunk_ids(chunks):
    last_page_id = None
    current_chunk_index = 0
    for chunk in chunks:
        source=chunk.metadata['source']
        if (source.endswith("pdf")):

            page = chunk.metadata.get("page")
            current_page_id = f"{source}:{page}"

            if current_page_id == last_page_id:
                current_chunk_index+=1 
            else:
                current_chunk_index=0

            chunk_id= f"{current_page_id}:{current_chunk_index}"
            last_page_id=current_page_id
            
            chunk.metadata['id']=chunk_id

        elif(source.endswith("csv")):
            show_id = ''

            match = re.search(r'^show_id:\s*(\S+)', str(chunk.page_content), re.MULTILINE)
            if match:
                show_id = match.group(1)

            chunk.metadata['id'] = f'{source}:{show_id}'

    return chunks
        
def add_to_chroma_db(chunks):
    db = Chroma(persist_directory=chroma_path,embedding_function=get_embedding_function())

    chunks_with_id = calculate_chunk_ids(chunks)
    existing_items = db.get()
    existing_id = set(existing_items['ids'])

    print(f"Current Items in ChromaDB: {len(existing_id)}")

    new_chunks = []
    for chunk in chunks_with_id:
        if chunk.metadata['id'] not in existing_id:
            new_chunks.append(chunk)
        # print("Test")
    
    if len(new_chunks):
        print(f"Items to be Added: {len(new_chunks)}")
        
        # Split new_chunks into batches of 500
        for i in range(0, len(new_chunks), 500):
            batch = new_chunks[i:i + 500]
            batch_ids = [chunk.metadata['id'] for chunk in batch]
            
            print(f"Adding batch {i // 500 + 1} with {len(batch)} items...")
            db.add_documents(batch, ids=batch_ids)
        
        print("All chunks added successfully.")

    else:
        print("No New Items to be Added")

if __name__ == "__main__":
    main()