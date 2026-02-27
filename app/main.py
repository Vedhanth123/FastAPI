from contextlib import asynccontextmanager

from dotenv import load_dotenv
from fastapi import FastAPI, HTTPException, Response, status
from fastapi.params import Body
from psycopg import connect
from psycopg.rows import dict_row, namedtuple_row
from sqlmodel import SQLModel, select

from .database import SessionDep, engine, lifespan
from .databasemodels import Posts

load_dotenv()

# ----------------------------------------------- FastAPI starting------------------------------------------
app = FastAPI(lifespan=lifespan)


# ------------------------------------- Getting all posts -------------------------------------------------
@app.get("/posts")
async def get_posts(
    session: SessionDep,
):  # name the functions as descriptive as possible.

    rows = session.exec(select(Posts)).all()
    return {"data": rows}
    # fast api will automatically convert the python dict to json


# If there are more than 1 functions to the same path then fastpi will give preference to the first path


# ------------------------------------- Getting single post -------------------------------------------------
@app.get("/posts/{post_id}")
async def get_post(post_id: int, response: Response, session: SessionDep):

    rows = session.exec(select(Posts), post_id)
    if rows:
        return {"data": rows}

    # response.status_code = status.HTTP_404_NOT_FOUND
    # return {"message":f"post with {post_id} was not found"}

    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail=f"post with id: {post_id} not found",
    )


# ------------------------------------- Creating a post -------------------------------------------------
@app.post("/posts", status_code=status.HTTP_201_CREATED)
async def posts(
    post: Posts, session: SessionDep
):  # => body of the http request will be send to this parameter. This line will basically extract all the fields from the body and will convert it into python dictionary

    session.add(post)
    session.commit()
    session.refresh(post)
    return post


# ------------------------------------- deleting a post -------------------------------------------------
@app.delete("/posts/{post_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_post(post_id: int, session: SessionDep):

    post = session.get(Posts, post_id)
    if not post:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"post with id: {post_id} not found",
        )
    session.delete(post)
    return {"data": post}


# hello
# ------------------------------------- updating a post -------------------------------------------------
@app.put("/posts/{post_id}", status_code=status.HTTP_201_CREATED)
async def update_post(post_id: int, session: SessionDep, updated_post: Posts):

    old_post = session.get(Posts, post_id)

    if not old_post:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"post with id: {post_id} not found",
        )

    update_dict = updated_post.model_dump(exclude_unset=True)

    # 3. Apply the updates to the database object
    for key, value in update_dict.items():
        setattr(old_post, key, value)

    session.add(old_post)
    session.commit()
    session.refresh(old_post)
    return old_post
