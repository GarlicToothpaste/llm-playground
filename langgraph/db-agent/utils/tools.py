from langchain.tools import tool
from sqlalchemy import create_engine, text
from sqlalchemy.engine import URL
import os
from pathlib import Path
from dotenv import load_dotenv

env_path = (Path(__file__).parent.parent / ".env").resolve()
load_dotenv(dotenv_path=env_path)  
print(env_path)

db_type = os.environ.get("DB_TYPE") 
driver = os.environ.get("DB_DRIVER")
username = os.environ.get("DB_USERNAME")
password = os.environ.get("DB_PASSWORD")
host = os.environ.get("DB_HOST")
database = os.environ.get("DATABASE")
port = os.environ.get("PORT") # Optional, defaults are often fine

if driver:
    drivername = f"{db_type}+{driver}"
else:
    drivername = db_type

DATABASE_URL = URL.create(
    drivername=drivername,
    username=username,
    password=password,
    host=host,
    database=database,
    port=port,
)

engine = create_engine(DATABASE_URL, echo=True) 

@tool
def show_items():
    """Shows all the items in the database"""
    try:
        with engine.connect() as connection:
            # result = connection.execute(text("SELECT 'connection successful'"))

            sql_statement = text("SELECT * FROM shop_inventory")
            result = connection.execute(sql_statement)
            results_as_dict = result.mappings().all()
            print(results_as_dict)
    except Exception as e:
        print(f"Connection failed: {e}")
    return(results_as_dict)

#TODO: Adds the Item Name, Description, and Available Stock to the DB
@tool
def add_item():
    """Adds an item to the database"""
    try:
        with engine.connect() as connection:

            sql_statement = text("INSERT INTO shop_inventory ( item_name, description, quantity) VALUES ('SQLALchemy Test', 'Sample Values lol', 15)")
            result = connection.execute(sql_statement)
            print(result)
            message = "Successfully Added to the Database"
    except Exception as e:
        print(f"Connection failed: {e}")
    return(message)

#TODO: Updates the Item Name, Description, and Available Stock to the DB
@tool
def update_item():
    """Updates details in the database"""
    print("Test")