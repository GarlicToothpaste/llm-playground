from langchain_community.utilities.sql_database import SQLDatabase
import os
from sqlalchemy import URL
from dotenv import load_dotenv
from pathlib import Path
from langchain_ollama import ChatOllama
env_path = Path(__file__).parent / ".env"
load_dotenv(dotenv_path=env_path)  

url_object = URL.create(
    drivername="mysql+pymysql",
    username=os.getenv("LOCAL_LLM_DB_USERNAME"),
    password=os.getenv("LOCAL_LLM_DB_PASSWORD"),
    host=os.getenv("LOCAL_LLM_DB_HOST"),
    port=os.getenv("LOCAL_LLM_DB_PORT"),
    database=os.getenv("LOCAL_LLM_DB_NAME")
    )

db = SQLDatabase.from_uri(url_object)

llm = ChatOllama(model="mistral-small:24b", temperature=0.3)
print(db.get_table_names())