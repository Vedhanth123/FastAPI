import os
from contextlib import asynccontextmanager
from typing import Annotated

from dotenv import load_dotenv
from fastapi import Depends, FastAPI
from sqlmodel import Session, SQLModel, create_engine

load_dotenv()

SQLALCHEMY_DATABASE_URL = os.getenv("SQLALCHEMY_DATABASE_URL")

# it will interact with the database It will establish the connection
engine = create_engine(SQLALCHEMY_DATABASE_URL)


# To talk to the database we have to make use of a session
def get_session():
    with Session(engine) as session:
        yield session


SessionDep = Annotated[Session, Depends(get_session)]


@asynccontextmanager
async def lifespan(app: FastAPI):
    # This is the "on startup" part
    print("🟢 App is Starting Up!")
    print("Creating tables...")
    SQLModel.metadata.create_all(engine)
    yield

    print("🛑 App is shutting down! Cleaning up resources...")
