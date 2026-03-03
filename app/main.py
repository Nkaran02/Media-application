from fastapi import FastAPI
from fastapi.params import Body
from pydantic import BaseModel
from typing import Optional
from random import randrange
from fastapi import requests,responses,Request, Response, status, HTTPException, Depends
import psycopg2
import time 
from psycopg2.extras import RealDictCursor
from sqlalchemy.orm import Session
from . import models, schemas
from . database import engine, get_db
from .import utils
from .routers import post, user, auth

models.Base.metadata.create_all(bind=engine)

app = FastAPI()

while True:
    try:
        conn = psycopg2.connect(
            host='localhost', 
            database='media', user='postgres', 
            password='Newpassword@123', 
            cursor_factory=RealDictCursor
            )
        cursor = conn.cursor()
        print("Database connections was successfull")
        break
    except Exception as error:
        print("Connection failed ", error)
        time.sleep(2)

@app.get("/")
def display():
    return {"message":"hello world"}

app.include_router(post.router)

app.include_router(user.router)

app.include_router(auth.router)

