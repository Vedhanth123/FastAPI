from datetime import datetime, time
from token import OP
from types import NoneType
from typing import Optional
from unittest.mock import Base

from click import Option
from psycopg import Timestamp
from sqlalchemy import false
from sqlmodel import Column, DateTime, Field, SQLModel, func


class BasePosts(SQLModel):
    title: str
    contents: str
    published: bool = False


class Posts(BasePosts, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    created_at: Optional[datetime] = Field(
        default=None,
        sa_column=Column(
            DateTime(timezone=True), nullable=False, server_default=func.now()
        ),
    )


class CreatePosts(BasePosts):
    pass


class UpdatePosts(BasePosts):
    title: Optional[str] = None
    contents: Optional[str] = None
    published: Optional[bool] = None


class PostResponse(BasePosts):
    pass
