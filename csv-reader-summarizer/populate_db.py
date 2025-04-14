import os 
from langchain.document_loaders import DirectoryLoader
from langchain_community.document_loaders.csv_loader import CSVLoader
# from pprint import pprint
import re
from get_embedding_function import get_embedding_function
from langchain_chroma import Chroma

dir_path = os.path.dirname(os.path.realpath(__file__))
directory_path = dir_path + '/data'
chroma_path = dir_path + '/chroma'

def main():
    data = load_documents()
    add_to_chroma_db(data)
    
def load_documents():
    loader = DirectoryLoader(directory_path, glob='**/*.csv', loader_cls=CSVLoader)
    data = loader.load()
    return data

def calculate_chunk_ids(chunks):
    for chunk in chunks:
        source=chunk.metadata['source']
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
    
    if len(new_chunks):
        print(f"Items to be Added: {len(new_chunks)}")
        new_chunk_ids=[chunk.metadata['id'] for chunk in new_chunks]
        db.add_documents(new_chunks, ids = new_chunk_ids)
    else:
        print("No New Items to be Added")

if __name__ == "__main__":
    main()