from datetime import datetime
from typing import Optional

from pydantic import EmailStr, conint
from sqlalchemy import ForeignKey, Integer
from sqlmodel import Column, DateTime, Field, Relationship, SQLModel, func


# ----------------------------------------- Users Table --------------------------------------------------
class BaseUsers(SQLModel):
    email: EmailStr
    name: str
    password: str


class Users(BaseUsers, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    email: EmailStr = Field(unique=True)
    password: str = Field(min_length=8)
    created_at: Optional[datetime] = Field(
        default=None,
        sa_column=Column(
            DateTime(timezone=True), nullable=False, server_default=func.now()
        ),
    )


class CreateUser(BaseUsers):
    pass


class UserResponse(SQLModel):
    id: int
    email: EmailStr
    name: str


class UserLogin(SQLModel):
    email: EmailStr
    password: str


# ----------------------------------------- Posts Table --------------------------------------------------
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
    user_id: int = Field(
        sa_column=Column(
            Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False
        )
    )

    user: "Users" = Relationship()


class CreatePosts(BasePosts):
    pass


class UpdatePosts(BasePosts):
    title: Optional[str] = None
    contents: Optional[str] = None
    published: Optional[bool] = None


class PostResponse(BasePosts):
    id: int
    user_id: int
    user: UserResponse


# ---------------------------------------------- Access token schema -------------------------------------------
class Token(SQLModel):
    access_token: str
    token_type: str


class TokenData(SQLModel):
    id: Optional[str] = None


# ---------------------------------------------- Votes table ------------------------------------------------
class Votes(SQLModel, table=True):
    user_id: int = Field(
        sa_column=Column(
            Integer, ForeignKey("users.id", ondelete="CASCADE"), primary_key=True
        ),
    )
    post_id: int = Field(
        sa_column=Column(
            Integer, ForeignKey("posts.id", ondelete="CASCADE"), primary_key=True
        ),
    )


class VoteRequest(SQLModel):
    post_id: int
    liked: conint(le=1)


# Create a schema for the combined data
class PostWithVotes(SQLModel):
    Posts: PostResponse  # This matches the SQLModel class name in the tuple
    votes: int
