import os
from dotenv import load_dotenv
from db_utils import *
load_dotenv()

#---0. META VARIABLE----
# a. database url
POSTGRES_DB_URL = f"""postgresql://{os.environ["USER"]}:{os.environ["PASSWORD"]}@{os.environ["HOST"]}:{os.environ["PORT"]}/{os.environ["DATABASE"]}"""
# b. table in which we will store the data
TABLE_NAME = "translation"
# b. query to create the table ( adjust the field in order to the csv)
Q_CREATE_TABLE = f"""
            CREATE TABLE IF NOT EXISTS {TABLE_NAME} (
                text_origin VARCHAR(1024),
                text_target VARCHAR(1024),
                extracted_at DATE,
                lang_origin VARCHAR(255),
                source_name VARCHAR(255),
                lang_target VARCHAR(255),
                source_type VARCHAR(255)
                )
            """
# c. get the csv path to load data
CSV_PATH = os.environ['CSV_PATH']
# c. separator 
SEP = ","
# c. header quote
HQUOTE= "}"

# d. constraint
Q_PRIMARY_KEY = f"""
            ALTER TABLE {TABLE_NAME}
            ADD id  SERIAL PRIMARY KEY
            """



def main()->None:
    # create the table 
    execute_sql(Q_CREATE_TABLE,POSTGRES_DB_URL)
    # import data
    copy_csv(CSV_PATH,POSTGRES_DB_URL,TABLE_NAME,SEP,HQUOTE)
    # # add constraint pk 
    execute_sql(Q_PRIMARY_KEY,POSTGRES_DB_URL)
main()