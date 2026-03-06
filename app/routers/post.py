from typing import List, Optional

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy import func
from sqlalchemy.orm import joinedload, selectinload
from sqlmodel import select

from app.database import SessionDep
from app.models import (
    CreatePosts,
    PostResponse,
    PostWithVotes,
    Posts,
    UpdatePosts,
    Users,
    Votes,
)
from app.oauth2 import get_current_user

# ----------------------------------------------------------------------------------------------
#                                         POSTS
# ----------------------------------------------------------------------------------------------

router = APIRouter(prefix="/posts", tags=["Posts"])


# ------------------------------------- Getting all posts -------------------------------------------------
# @router.get("/", response_model=List[PostResponse])
@router.get("/", response_model=List[PostWithVotes])
async def get_posts(
    session: SessionDep,
    limit: int = 10,
    skip: int = 0,
    search: Optional[str] = "",
):  # name the functions as descriptive as possible.         # query parameter

    result = session.exec(
        select(Posts, func.count(Votes.post_id).label("votes"))
        .join(Votes, Posts.id == Votes.post_id, isouter=True)
        .group_by(Posts.id)
        .filter(Posts.title.contains(search))
        .limit(limit)
        .offset(skip)
        # .options(selectinload(Posts.user)) # This is given by gemini. I have to understand it...
    ).all()

    return result

    # return result
    # fast api will automatically convert the python dict to json


# If there are more than 1 functions to the same path then fastpi will give preference to the first path


# ------------------------------------- Getting single post -------------------------------------------------
@router.get("/{post_id}", response_model=PostWithVotes)  # path operation
async def get_post(post_id: int, session: SessionDep):

    rows = session.exec(
        select(Posts, func.count(Votes.post_id).label("votes"))
        .join(Votes, Posts.id == Votes.post_id, isouter=True)
        .group_by(Posts.id)
        .filter(Posts.id == post_id)
    ).first()
    if rows:
        return rows

    print(rows)
    # response.status_code = status.HTTP_404_NOT_FOUND
    # return {"message":f"post with {post_id} was not found"}

    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail=f"post with id: {post_id} not found",
    )


# ------------------------------------- Creating a post -------------------------------------------------
@router.post("/", status_code=status.HTTP_201_CREATED, response_model=PostResponse)
async def posts(
    post: CreatePosts,
    session: SessionDep,
    current_user: dict = Depends(get_current_user),
):  # => body of the http request will be send to this parameter. This line will basically extract all the fields from the body and will convert it into python dictionary

    print(current_user)
    post = post.model_dump()
    post.update({"user_id": current_user.id})
    # we need to convert from CreatePost object to Post object
    post = Posts.model_validate(post)
    session.add(post)
    session.commit()
    session.refresh(post)
    return post


# ------------------------------------- deleting a post -------------------------------------------------
@router.delete(
    "/{post_id}",
    status_code=status.HTTP_204_NO_CONTENT,
)
async def delete_post(
    post_id: int,
    session: SessionDep,
    response_model=PostResponse,
    current_user: dict = Depends(get_current_user),
):

    post = session.get(Posts, post_id)
    if not post:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"post with id: {post_id} not found",
        )
    if current_user.id != post.user_id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail=f"user id {post.user_id} cannot delete the post",
        )
    session.delete(post)
    session.commit()
    return post


# hello
# ------------------------------------- updating a post -------------------------------------------------
@router.put(
    "/{post_id}", status_code=status.HTTP_201_CREATED, response_model=PostResponse
)
async def update_post(
    post_id: int,
    session: SessionDep,
    updated_post: UpdatePosts,
    current_user: dict = Depends(get_current_user),
):

    old_post = session.get(Posts, post_id)

    if not old_post:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"post with id: {post_id} not found",
        )

    if current_user.id != old_post.user_id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail=f"user id {old_post.user_id} cannot delete the post",
        )

    update_dict = updated_post.model_dump(
        exclude_unset=True
    )  # exclude_unset=True is what is allowing me to do Patch update not just put update.

    # 3. Apply the updates to the database object
    for key, value in update_dict.items():
        setattr(old_post, key, value)

    session.add(old_post)
    session.commit()
    session.refresh(old_post)
    return old_post
