from datetime import datetime
from pydantic import BaseModel
from pydantic import EmailStr
from typing import Literal
from typing import Optional



class PostBase(BaseModel):
    title: str
    content: str
    published: bool = True

    class Config:
        from_attributes = True


class UserBase(BaseModel):
    first_name: str
    last_name: str
    email: EmailStr

    class Config:
        from_attributes = True


class PostCreate(PostBase):
    pass

class UserCreate(UserBase):
    password: str


class PostOut(PostBase):
    id: int
    created_at: datetime
    owner_id: int
    owner: UserBase

    class Config:
        from_attributes = True


class PostResponse(BaseModel):
    id: int
    title: str 
    content: str 
    published: bool 
    created_at: datetime 
    owner_id: int
    owner: UserBase 
    votes: int = 0

    class Config:
        from_attributes = True


class UserOut(UserBase):
    id: int
    created_at: datetime

    class Config:
        from_attributes = True


class UserLogin(BaseModel):
    email: EmailStr
    password: str

class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    id: Optional[str] = None

class Vote(BaseModel):
    post_id: int
    direction: Literal[0, 1]