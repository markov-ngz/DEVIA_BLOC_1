import psycopg2
from psycopg2.extras import RealDictCursor

def execute_sql(sql:str, url:str)->None:
    """
    
    """
    try : 
        conn = psycopg2.connect(url, cursor_factory = RealDictCursor)
        conn.autocommit = True
        cursor = conn.cursor() 

        cursor.execute(sql) 

        cursor.close()

        print("SQL QUERY EXECUTION SUCCEEDED")

    except psycopg2.Error as e:
        print("Error:", e)


def copy_csv(file_path:str,url:str,table_name:str, sep:str, hquote:str)->None:
    """
    
    """
    query = f"""copy {table_name} FROM stdin WITH DELIMITER '{sep}' CSV HEADER QUOTE '{hquote}';"""
    try:
        with open(file_path, 'r', encoding="utf-8") as f:
                conn = psycopg2.connect(url, cursor_factory = RealDictCursor)
                conn.autocommit = True
                cursor = conn.cursor()     

                cursor.copy_expert(
                        query,
                        f
                )
                cursor.close()
    except psycopg2.Error as e:
            print("Error:", e)