from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base, sessionmaker
from sqlalchemy.orm import Session
import psycopg2
from psycopg2.extras import RealDictCursor
import time
from app.config import settings
from dotenv import load_dotenv


SQLALCHEMY_DATABASE_URL = f"postgresql://{settings.database_username}:{settings.database_password}@{settings.database_hostname}:{settings.database_port}/{settings.database_name}"

engine = create_engine(SQLALCHEMY_DATABASE_URL)

SessionLocal = sessionmaker( bind=engine, autocommit=False, autoflush=False)

Base = declarative_base()

# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

""" while True : 

    try:
        conn = psycopg2.connect(host = 'localhost',database='fastapi', user='postgres', password='iakoutsk50!MQW', cursor_factory=RealDictCursor)
        cursor = conn.cursor()
        print("Database Connection was successfull !")
        break
    except Exception as error:
        print("Connecting to database failed")
        print("Error : ", error)
        time.sleep(2) """