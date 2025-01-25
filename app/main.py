from fastapi import FastAPI, Response, status,HTTPException, Depends
from fastapi.params import Body
from pydantic import BaseModel
from typing import Optional, List
import psycopg2
from psycopg2.extras import RealDictCursor
from .routers import user,post,auth,vote
from .config import setting
from fastapi.middleware.cors import CORSMiddleware

# using orm now
from sqlalchemy.orm import Session 
from . import models,schemas,utilis
from .database import engine, get_db

#models.Base.metadata.create_all(bind=engine)  now alembic is handling this shitt


origins = ["*"]

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# try:
#     conn=psycopg2.connect(host='localhost',database='fastapi',user='postgres',password='aman1', cursor_factory=RealDictCursor)
#     cursor=conn.cursor();
#     print("databse connected susseful")
# except Exception as error:
#     print("Connection failed")
#     print(error)
# 
#       for connecting to raw sql






app.include_router(vote.router)
app.include_router(post.router)
app.include_router(user.router)
app.include_router(auth.router)

print("Running main.py")


@app.get("/")
async def root():
    return {"message":"Heelo "}
