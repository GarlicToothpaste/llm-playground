import os 
from langchain.document_loaders import DirectoryLoader
from langchain_community.document_loaders.csv_loader import CSVLoader

dir_path = os.path.dirname(os.path.realpath(__file__))
directory_path = dir_path + '/data/netflix_shows.csv'

def load_documents():
    #TODO: Implement a Directory Loader
    # loader = DirectoryLoader(directory_path, glob='*.csv')
    loader = CSVLoader(file_path=directory_path)
    data = loader.load()
    print(data)
    return data

print(load_documents())