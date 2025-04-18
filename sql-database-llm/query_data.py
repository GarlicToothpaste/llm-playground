from langchain_community.utilities.sql_database import SQLDatabase
import os
from sqlalchemy import URL
from dotenv import load_dotenv
from pathlib import Path
from langchain_ollama import ChatOllama
from langchain_experimental.sql import SQLDatabaseChain
from langchain.schema import HumanMessage, SystemMessage
from langchain_core.prompts import HumanMessagePromptTemplate

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
llm = ChatOllama(model="mistral-small:24b", temperature=0.3, stop_sequence=["\nSQLQuery:"])

db_chain = SQLDatabaseChain.from_llm(llm, db, verbose=True)

def retrieve_from_db(query : str):
    #TODO: The error is here. Mistral Outputs a paragraph instead of an SQL Query so the db_chain.invoke fails
    db_context = db_chain.invoke(input=query)
    db_context = db_context['result'].strip()
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

    human_prompt = HumanMessagePromptTemplate(PROMPT_TEMPLATE)
    messages = [ SystemMessage(system_message),
                human_prompt.format(human_input=query, db_context=db_context)
                ]
    response= llm(messages).content
    print(response)
    return response

generate_query("Which artists in australia has the most amount of monthly listeners?")