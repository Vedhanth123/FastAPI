from typing import List

from dotenv import load_dotenv
from fastapi import FastAPI, HTTPException, status
from passlib.context import CryptContext
from sqlmodel import select
from starlette.status import HTTP_404_NOT_FOUND

from app.routers import auth, post, user
from app.utils import hash_password

from .database import SessionDep, lifespan
from .models import (
    CreatePosts,
    CreateUser,
    PostResponse,
    Posts,
    UpdatePosts,
    UserResponse,
    Users,
)

load_dotenv()

# ----------------------------------------------- FastAPI starting------------------------------------------
app = FastAPI(lifespan=lifespan)

app.include_router(post.router)
app.include_router(user.router)
app.include_router(auth.router)
