from typing import List

from dotenv import load_dotenv
from fastapi import FastAPI, HTTPException, Response, status
from sqlmodel import SQLModel, select

from .database import SessionDep, engine, lifespan
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


# ----------------------------------------------------------------------------------------------
#                                         POSTS
# ----------------------------------------------------------------------------------------------


# ------------------------------------- Getting all posts -------------------------------------------------
@app.get("/posts", response_model=List[PostResponse])
async def get_posts(
    session: SessionDep, response_model=PostResponse
):  # name the functions as descriptive as possible.

    rows = session.exec(select(Posts)).all()
    return rows
    # fast api will automatically convert the python dict to json


# If there are more than 1 functions to the same path then fastpi will give preference to the first path


# ------------------------------------- Getting single post -------------------------------------------------
@app.get("/posts/{post_id}", response_model=PostResponse)
async def get_post(post_id: int, session: SessionDep):

    rows = session.get(Posts, post_id)
    if rows:
        return rows

    # response.status_code = status.HTTP_404_NOT_FOUND
    # return {"message":f"post with {post_id} was not found"}

    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail=f"post with id: {post_id} not found",
    )


# ------------------------------------- Creating a post -------------------------------------------------
@app.post("/posts", status_code=status.HTTP_201_CREATED, response_model=PostResponse)
async def posts(
    post: CreatePosts, session: SessionDep
):  # => body of the http request will be send to this parameter. This line will basically extract all the fields from the body and will convert it into python dictionary

    # we need to convert from CreatePost object to Post object
    post = Posts.model_validate(post)
    session.add(post)
    session.commit()
    session.refresh(post)
    return post


# ------------------------------------- deleting a post -------------------------------------------------
@app.delete(
    "/posts/{post_id}",
    status_code=status.HTTP_204_NO_CONTENT,
)
async def delete_post(post_id: int, session: SessionDep, response_model=PostResponse):

    post = session.get(Posts, post_id)
    if not post:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"post with id: {post_id} not found",
        )
    session.delete(post)
    session.commit()
    return post


# hello
# ------------------------------------- updating a post -------------------------------------------------
@app.put(
    "/posts/{post_id}", status_code=status.HTTP_201_CREATED, response_model=PostResponse
)
async def update_post(post_id: int, session: SessionDep, updated_post: UpdatePosts):

    old_post = session.get(Posts, post_id)

    if not old_post:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"post with id: {post_id} not found",
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


# ----------------------------------------------------------------------------------------------
#                                         Users
# ----------------------------------------------------------------------------------------------


@app.post("/register", status_code=status.HTTP_201_CREATED, response_model=UserResponse)
def create_user(user: CreateUser, session: SessionDep):
    
    statement = select(Users).where(Users.email == user.email)
    data = session.exec(statement).first()

    if data:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail=f"{user.email} already exists!",
        )

    user = Users.model_validate(user)

    session.add(user)
    session.commit()
    session.refresh(user)
    return user

