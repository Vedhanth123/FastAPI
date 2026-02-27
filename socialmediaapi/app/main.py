from contextlib import asynccontextmanager

from dotenv import load_dotenv
from fastapi import FastAPI, HTTPException, Response, status
from fastapi.params import Body
from psycopg import connect
from psycopg.rows import dict_row, namedtuple_row
from sqlmodel import SQLModel

from .database import SessionDep, engine, lifespan
from .databasemodels import Posts

load_dotenv()

# ----------------------------------------------- FastAPI starting------------------------------------------

app = FastAPI(lifespan=lifespan)


# ----------------------------------------- Testing Database connection ----------------------------------
@app.get("/sql")
async def get_things(session: SessionDep):
    print("hey.. bastard")
    return {"Status": "Success"}


# ------------------------------------- Getting all posts -------------------------------------------------
@app.get("/posts")
async def get_posts():  # name the functions as descriptive as possible.

    posts = curr.execute("SELECT * FROM posts")
    rows = posts.fetchall()
    for row in rows:
        print(row)

    return {"data": rows}
    # fast api will automatically convert the python dict to json


# If there are more than 1 functions to the same path then fastpi will give preference to the first path


# ------------------------------------- Getting single post -------------------------------------------------
@app.get("/posts/{post_id}")
async def get_post(post_id: int, response: Response):

    posts = curr.execute("SELECT * FROM posts where id = %s", (post_id,))
    data = posts.fetchone()
    print(data)
    return {"data": data}

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
async def delete_post(post_id: int):

    STATEMENT = "DELETE FROM posts WHERE id = %s RETURNING *"
    id = post_id
    curr.execute(STATEMENT, (id,))
    deleted_post = curr.fetchone()
    conn.commit()
    # data = curr.fetchone()
    # print(data)

    if not deleted_post:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"post with id: {post_id} not found",
        )

    return {"data": deleted_post}


# hello
# ------------------------------------- updating a post -------------------------------------------------
@app.put("/posts/{post_id}", status_code=status.HTTP_201_CREATED)
async def update_post(post_id: int, updated_post: BasePost):

    STATEMENT = """UPDATE posts SET title = %s,
                    contents = %s,
                    published = %s
                    where id = %s
                    RETURNING *
                """
    payload = (
        updated_post.title,
        updated_post.content,
        updated_post.published,
        post_id,
    )
    curr.execute(STATEMENT, payload)
    data = curr.fetchone()
    conn.commit()

    if not data:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"post with id: {post_id} not found",
        )

    return {"data": data}
