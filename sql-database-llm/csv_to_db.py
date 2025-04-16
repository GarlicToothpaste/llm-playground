from sqlalchemy import URL
from sqlalchemy import create_engine
import pandas as pd
import os
from dotenv import load_dotenv
from pathlib import Path

env_path = Path(__file__).parent / ".env"
load_dotenv(dotenv_path=env_path)  

def main():
    csv_path = '/home/adrian/Desktop/Personal Projects/llm-playground/sql-database-llm/data/Spotify_2024_Global_Streaming_Data.csv'
    table_name = "spotify_streaming_2024"
    csv_to_db (csv_path=csv_path, table_name=table_name)

def csv_to_db(csv_path: str , table_name: str):
    data = pd.read_csv(csv_path)

    url_object = URL.create(
        drivername="mysql+pymysql",
        username=os.getenv("LOCAL_LLM_DB_USERNAME"),
        password=os.getenv("LOCAL_LLM_DB_PASSWORD"),
        host=os.getenv("LOCAL_LLM_DB_HOST"),
        port=os.getenv("LOCAL_LLM_DB_PORT"),
        database=os.getenv("LOCAL_LLM_DB_NAME")
    )
    engine = create_engine(url_object)
    data.to_sql(table_name, con=engine, if_exists='replace', index=False)

    return "Success"

if __name__ == "__main__":
    main()