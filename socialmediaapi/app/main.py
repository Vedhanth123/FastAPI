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
    
    return rows
      # fast api will automatically convert the python dict to json


# If there are more than 1 functions to the same path then fastpi will give preference to the first path


# ------------------------------------- Getting single post -------------------------------------------------
@app.get("/posts/{post_id}")
async def get_post(post_id: int, response: Response):

    for post in my_posts:
        if post["id"] == post_id:
            return {"data": post}

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

    for idx, post in enumerate(my_posts):
        if post["id"] == post_id:
            my_posts.pop(idx)
            return Response(status_code=status.HTTP_204_NO_CONTENT)

    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail=f"post with id: {post_id} not found",
    )


# hello
# ------------------------------------- updating a post -------------------------------------------------
@app.put("/posts/{post_id}", status_code=status.HTTP_201_CREATED)
async def update_post(post_id: int, updated_post: BasePost):

    for post in my_posts:
        if post["id"] == post_id:
            updated_post_dict = updated_post.model_dump()
            post["title"] = updated_post_dict["title"]
            post["content"] = updated_post_dict["content"]
            post["rating"] = updated_post_dict["rating"]
            post["published"] = updated_post_dict["published"]
            return Response(status_code=status.HTTP_201_CREATED)

    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail=f"post with id: {post_id} not found",
    )
