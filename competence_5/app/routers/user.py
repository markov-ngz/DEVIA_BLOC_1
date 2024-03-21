from app import models, schemas, utils
from fastapi import FastAPI, Response, status,  HTTPException, Depends, APIRouter
from sqlalchemy.orm import Session
from app.database import get_db

router = APIRouter(
    prefix="/users",
    tags=['Users']
)

@router.post("/", status_code = status.HTTP_201_CREATED,response_model=schemas.UserOut) 
def create_user(user : schemas.UserCreate, db :Session = Depends(get_db)):

    #hash the password - user.password 
    hashed_pwd = utils.hash(user.password)
    user.password = hashed_pwd

    new_user = models.User(**user.dict())
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user
