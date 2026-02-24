from random import randrange

from fastapi import FastAPI, HTTPException, Response, status
from fastapi.params import Body

from data import my_posts
from models import BasePost
import json

from psycopg import connect
from dotenv import load_dotenv
import os
from psycopg.rows import dict_row, namedtuple_row
import time

load_dotenv()

# this is same like the documentation
app = FastAPI()

# path and route are basically same
# path operation


# variables
DB_HOSTNAME = os.getenv('DB_HOSTNAME')
DB_PASSWORD = os.getenv('DB_PASSWORD')
DB_USERNAME = os.getenv('DB_USERNAME')
DB = os.getenv('DB')
DB_PORT = os.getenv('DB_PORT')

# --------------------------------------- Database connection ---------------------------------------------
while(True):
    try:
        conn = connect(host=DB_HOSTNAME, dbname=DB, user=DB_USERNAME, password=DB_PASSWORD, row_factory=dict_row)
        curr = conn.cursor(row_factory=namedtuple_row)
        print(F"database connected successfully")
        break
    except Exception as e:
        print(f"connection to database failed")
        print(f"Error as {e}")
        time.sleep(2)

# ------------------------------------- Getting all posts -------------------------------------------------
@app.get("/posts")
async def get_posts():  # name the functions as descriptive as possible.

    posts = curr.execute("SELECT * FROM posts")
    rows = posts.fetchall()
    for row in rows:
        print(row)
    
    return {
        "data": rows
    }
      # fast api will automatically convert the python dict to json


# If there are more than 1 functions to the same path then fastpi will give preference to the first path


# ------------------------------------- Getting single post -------------------------------------------------
@app.get("/posts/{post_id}")
async def get_post(post_id: int, response: Response):


    posts = curr.execute("SELECT * FROM posts where id = %s", (post_id,))
    data = posts.fetchone()
    print(data)
    return {
        "data": data
    }

    # response.status_code = status.HTTP_404_NOT_FOUND
    # return {"message":f"post with {post_id} was not found"}

    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail=f"post with id: {post_id} not found",
    )


# ------------------------------------- Creating a post -------------------------------------------------
@app.post("/posts", status_code=status.HTTP_201_CREATED)
async def posts(
    post: BasePost,
):  # => body of the http request will be send to this parameter. This line will basically extract all the fields from the body and will convert it into python dictionary

    INSERT_STATEMENT = "INSERT INTO posts (title, contents, published) VALUES (%s, %s, %s) RETURNING *"
    VALUES = (post.title, post.content, post.published)

    curr.execute(INSERT_STATEMENT, VALUES)
    new_post = curr.fetchone()
    conn.commit()

    return {"data": new_post}  # automatically converts into json


# ------------------------------------- deleting a post -------------------------------------------------
@app.delete("/posts/{post_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_post(post_id: int):

    STATEMENT = "DELETE FROM posts WHERE id = %s RETURNING *"
    id = post_id
    curr.execute(STATEMENT, (id, ))
    deleted_post = curr.fetchone()
    conn.commit()
    # data = curr.fetchone()
    # print(data)

    if(not deleted_post):
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"post with id: {post_id} not found",
        )
    
    return {
        "data":deleted_post
    }


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
    payload = (updated_post.title, updated_post.content, updated_post.published, post_id)
    curr.execute(STATEMENT, payload)
    data = curr.fetchone()
    conn.commit()

    if(not data):
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"post with id: {post_id} not found",
        )

    return {
        "data":data
    }
