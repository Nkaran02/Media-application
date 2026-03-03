from fastapi import requests,responses,Request, Response, status, HTTPException, Depends, APIRouter
from typing import Optional, List
from .. import models, schemas, utils
from sqlalchemy.orm import Session
from ..database import engine, get_db

router = APIRouter(
    tags=['Users']
)

@router.get("/users", status_code=status.HTTP_200_OK, response_model=List[schemas.UserData])
def get_all_user(db:Session = Depends(get_db)):
    allusers = db.query(models.User).all()
    return allusers


@router.post("/create_users", status_code=status.HTTP_201_CREATED, response_model=schemas.UserData)
def create_user(user: schemas.UserCreate, db: Session = Depends(get_db)):

    
    if not user.password:
        raise HTTPException(status_code=400, detail="Password is required")

    password_bytes = user.password.encode("utf-8")[:72]
    safe_password = password_bytes.decode("utf-8", errors='ignore')

    hashed_password = utils.hash(user.password)
    user.password = hashed_password

    new_user = models.User(**user.dict())
    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    return new_user

@router.get("/user/{id}", response_model=schemas.UserData)
def get_user(id: int, db:Session = Depends(get_db)):
    user_by_id = db.query(models.User).filter(models.User.id == id).first()

    if not user_by_id:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"User with id {id} was not found")
    
    return user_by_id