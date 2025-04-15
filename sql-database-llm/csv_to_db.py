from sqlalchemy import URL
from sqlalchemy import create_engine
import pandas as pd
import os
from dotenv import load_dotenv
from pathlib import Path

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

engine = create_engine(url_object)

df = pd.DataFrame({
    'id': [1, 2],
    'name': ['Alice', 'Bob']
})

df.to_sql('your_table_name', con=engine, if_exists='replace', index=False)