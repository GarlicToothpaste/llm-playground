from langchain_community.utilities.sql_database import SQLDatabase
import os
from sqlalchemy import URL
from dotenv import load_dotenv
from pathlib import Path
from langchain_ollama import ChatOllama
from langchain_experimental.sql import SQLDatabaseChain
from langchain.schema import HumanMessage, SystemMessage
from langchain_core.prompts import HumanMessagePromptTemplate
from langchain_openai import ChatOpenAI

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

llm = ChatOpenAI( temperature=0, api_key=os.getenv("OPENAI_KEY"))

db_chain = SQLDatabaseChain.from_llm(llm, db, verbose=True)

def retrieve_from_db(query : str):
    db_context = db_chain(query)
    print(db_context)
    return db_context

def generate_query(query : str):
    db_context= retrieve_from_db(query)

    system_message=""" You are a Data Analyst Working for Spotify. You have to answer a user's queries and provide relevant information and insights.
    Here is an Example:

    Input:
    Which artist and album has the most number of Monthly Streamers in Japan?

    Context:
    The artists with the most number of monthly listeners are the following:
    1. BLACKPINK (BORN PINK)- 99.8M
    2. Doja Cat (Scarlet) - 97.52M
    3. Post Malone (Austin) - 96.33M

    Output:
    The artists and albums with the most amount of monthly listeners in Japan are Blackpink (BORN PINK) - 99.8M, Doja Cat (Scarlet) - 97.5M, and Post Malone (Austin) - 96.33M 
    """

    PROMPT_TEMPLATE= """
    Input:
    {human_input}

    Context:
    {db_context}

    Output:
    """

    human_prompt = HumanMessagePromptTemplate.from_template(PROMPT_TEMPLATE)
    messages = [ SystemMessage(system_message),
                human_prompt.format(human_input=query, db_context=db_context)
                ]
    response= llm(messages).content
    print(response)
    return response

#Correct
# generate_query("Which artists in australia has the most amount of monthly listeners?")

#TODO: It returns the top in a country, not worldwide. Make it aggregate.
# generate_query("What album is the most listened to worldwide?")

#Correct
generate_query("What country does BTS have the highest amount of total streams regardless of the album?")