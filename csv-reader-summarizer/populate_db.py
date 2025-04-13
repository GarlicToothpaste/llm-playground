import os 
from langchain.document_loaders import DirectoryLoader
from langchain_community.document_loaders.csv_loader import CSVLoader
from pprint import pprint
import re
dir_path = os.path.dirname(os.path.realpath(__file__))
directory_path = dir_path + '/data'

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
        

# pprint(load_documents())
pprint(calculate_chunk_ids(load_documents()))