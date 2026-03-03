from pydantic import BaseModel, ConfigDict,EmailStr, validator
from datetime import datetime
from typing import *

class PostBase(BaseModel):
    title : str
    content : str
    relesed: bool = True
    modified : Optional[str] = None
    
class PostCreate(PostBase):
    pass

class UserCreate(BaseModel):
    name: str
    email: EmailStr
    password: str

    @validator("password")
    def validate_password_length(cls, v):
        if not v or v.strip() == "":
            raise ValueError("Password cannot be empty")
        if len(v.encode("utf-8")) > 72:
            raise ValueError("Password too long (max 72 bytes in UTF-8)")
        return v



class ReturnResponse(BaseModel):
    title: str
    content: str
    created_at : datetime

    model_config = ConfigDict(from_attributes=True)
    
class UserData(BaseModel):
    id: int
    name:str
    email : EmailStr
    created_at : datetime
    model_config = ConfigDict(from_attributes=True)

class UserLogin(BaseModel):
    email: EmailStr
    password : str

class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    id: Optional[int] = True
    
