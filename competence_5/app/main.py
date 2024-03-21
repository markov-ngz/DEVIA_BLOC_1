import os, sys
sys.path.insert(0, os.path.abspath(".."))
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app import models
from app.database import engine
from app.routers import  user, auth, translation
from app.config import settings

# models.Base.metadata.create_all(bind=engine)

app = FastAPI()

origins = ["127.0.0.1, localhost"]
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["GET,POST"],
    allow_headers=["*"],
)

app.include_router(user.router)
app.include_router(auth.router)
app.include_router(translation.router)

@app.get("/",status_code=200)
def root():
    return {"message":"welcome to my api"}


   
