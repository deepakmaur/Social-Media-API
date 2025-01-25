from pydantic import BaseModel,EmailStr,Field
from datetime import datetime
from typing import Optional
from pydantic.types import conint

class PostBase(BaseModel):
    title:str
    content:str
    published:bool = True           # providing defalut value of true
    # rating: Optional[int]=None

class PostCreate(PostBase):
    pass

class UserName(BaseModel):
    id:int
    email:EmailStr


class Post(PostBase):
    created_at:datetime
    id:int
    owner_id:int
    owner:UserName

    class Config:
        from_attributes = True

class PostOut(BaseModel):
    Post: Post
    votes: int

    class Config:
        orm_mode = True



class UserCreate(BaseModel):
    email:EmailStr
    password:str


class UserLogin(BaseModel):
    email:EmailStr
    password:str

class UserOut(BaseModel):
    id:int
    email:EmailStr
    created_at:datetime

    class Config:
        from_attributes = True



class Token(BaseModel):
    access_token:str
    token_type:str
    

class TokenData(BaseModel):
    id:Optional[str]=None


class Vote(BaseModel):
    post_id: int
    dir: int = Field(ge=0, le=1)