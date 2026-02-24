from typing import Annotated

from fastapi import Depends, FastAPI, HTTPException, Query
from sqlmodel import Field, Session, SQLModel, create_engine, select

from dotenv import load_dotenv
import os

load_dotenv() 

SQLALCHEMY_DATABASE_URL = os.getenv('SQLALCHEMY_DATABASE_URL')

# it will interact with the database It will establish the connection
engine = create_engine(SQLALCHEMY_DATABASE_URL)

# To talk to the database we have to make use of a session
def get_session():
    with Session(engine) as session:
        yield session

SessionDep = Annotated[Session, Depends(get_session)]

# Code below omitted 👇