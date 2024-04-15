import os
from dotenv import load_dotenv
from db_utils import *
from sql_queries import *
from datetime import datetime
load_dotenv(".env", override=True)

now = datetime.now().strftime("%H:%M:%S")
#---0. META VARIABLE----
# a. database url
POSTGRES_DB_URL = f"""postgresql://{os.environ["USER"]}:{os.environ["PASSWORD"]}@{os.environ["HOST"]}:{os.environ["PORT"]}/{os.environ["DATABASE"]}"""


# b. get the csv path to load data
CSV_PATH = os.environ['CSV_PATH']
# c. separator 
SEP = ","
# d. header quote
HQUOTE= "}"

def model_db(POSTGRES_DB_URL:str)->None:
    # create the  temporary table 
    execute_sql(Q_CREATE_TABLE,POSTGRES_DB_URL)
    print(f"[{now}] : Temporary table created ")
    # create 3 tables : source, languages, translations
    execute_sql(CREATE_TABLE_SOURCE,POSTGRES_DB_URL)
    print(f"[{now}] : Source table created ")
    execute_sql(CREATE_TABLE_LANGUAGE,POSTGRES_DB_URL)
    print(f"[{now}] : Language table created ")
    execute_sql(CREATE_TABLE_TRANSLATIONS,POSTGRES_DB_URL)
    print(f"[{now}] : Translation table created ")
    # create a view for the API to easily get data
    execute_sql(CREATE_VIEW,POSTGRES_DB_URL)
    print(f"[{now}] : View created ")

def insert_data(CSV_PATH:str,POSTGRES_DB_URL:str)->None:
    # import data
    copy_csv(CSV_PATH,POSTGRES_DB_URL,TEMP_TABLE_NAME,SEP,HQUOTE)

    # insert data into those 
    execute_sql(INSERT_LANGUAGES,POSTGRES_DB_URL)
    print(f"[{now}] : Languages data inserted ")
    execute_sql(INSERT_SOURCE,POSTGRES_DB_URL)
    print(f"[{now}] : Sources data inserted ")
    execute_sql(INSERT_TRANSLATIONS,POSTGRES_DB_URL)
    print(f"[{now}] : Translations data inserted  ")

    # delete the temporary data 
    execute_sql(DELETE_TEMP, POSTGRES_DB_URL)
    print(f"[{now}] : Temporary data deleted ")

def main(CSV_PATH:str,POSTGRES_DB_URL:str, setup_database:bool=False )->None:
    if setup_database:
        model_db(POSTGRES_DB_URL)
    insert_data(CSV_PATH,POSTGRES_DB_URL)
    print("Data Successfully Imported")


    
main(CSV_PATH, POSTGRES_DB_URL, True)