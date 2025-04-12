import os 
from langchain.document_loaders import DirectoryLoader
from langchain_community.document_loaders.csv_loader import CSVLoader
from pprint import pprint
dir_path = os.path.dirname(os.path.realpath(__file__))
directory_path = dir_path + '/data'

def load_documents():
    loader = DirectoryLoader(directory_path, glob='**/*.csv', loader_cls=CSVLoader)
    data = loader.load()
    return data



pprint(load_documents())