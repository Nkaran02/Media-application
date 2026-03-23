from fastapi import FastAPI
from fastapi.params import Body
from pydantic import BaseModel
from typing import Optional
from random import randrange
from fastapi import requests,responses,Request, Response, status, HTTPException, Depends
from sqlalchemy.orm import Session
from . import models, schemas
from . database import engine, get_db
from .import utils
from .routers import post, user, auth, vote

models.Base.metadata.create_all(bind=engine)

app = FastAPI()

@app.get("/")
def display():
    return {"message":"hello world"}

app.include_router(post.router)

app.include_router(user.router)

app.include_router(auth.router)

app.include_router(vote.router)


