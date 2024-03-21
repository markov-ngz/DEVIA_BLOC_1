import psycopg2
from psycopg2.extras import RealDictCursor
import os
import os 
from dotenv import load_dotenv
import pandas as pd
from datetime import datetime
from tools.save_raw import try_and_save

# permet de charger l'ensemble des variables d'environnements
load_dotenv()


def database_extraction()->pd.DataFrame:
    """

    """
    try:
        conn = psycopg2.connect(host = os.environ['HOST'],database=os.environ['DATABASE'],user=os.environ['USER'], password=os.environ['PASSWORD']) 
        conn.autocommit = True
        cursor = conn.cursor() 
        query = "SELECT fr_text, pl_text FROM french_polish_tatoeba LIMIT 10;"

        cursor.execute(query)

        data = cursor.fetchall()


        conn.commit() 
        conn.close() 
    except psycopg2.Error as e:
        print("Error:", e)


    now = datetime.now().strftime("%Y-%m-%d")
    raw_df_db  = pd.DataFrame(data, columns=["text_origin","text_target"])
    raw_df_db["lang_origin"] = "french"
    raw_df_db["lang_target"] = "polish"
    raw_df_db["source"] = "DATABASE_NAME"
    raw_df_db["source_type"] = "database"
    raw_df_db["created_at"] = now


    return raw_df_db

