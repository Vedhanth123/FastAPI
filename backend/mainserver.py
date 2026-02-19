# THis file contains learnings from https://www.youtube.com/watch?v=rvFsGRvj9jo

# let's creata a simple todo list api


from enum import IntEnum
from typing import List, Optional

from data import getData, sendData
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field
from userdefinedmodels import Priority, TodoCreate, TodoItem, TodoUpdate

api = FastAPI()

FILE_NAME = "test_backend_todolist.json"


# ------------------------------------- Base path ---------------------------------------
# GET, POST, PUT (updating), DELETE
# @api.get("/")
# def index():
#     return {"msg": "Hey joker!"}


# We can also define sync and async endpoints.

"""
# async endopoint example (only used for IO bounds for example interacting with the database.)
@api.get('/getdata')
async def getData():
    # This isu 
"""
# creating endpoints for getting all todoes, creating, updating, deleting (basic CRUD operations)


@api.get("/")
def init_todo():

    sendData(
        FILE_NAME,
        TodoItem(
            todo_id=1,
            todo_name="dummy",
            todo_description="DUMMY",
            pri=Priority.LOW,
            completed=False,
        ).model_dump(),
    )


# ----------------------------- Path parameter fetch a single todo -------------------------------------
# get endpoint
@api.get("/todos/{todo_id}", response_model=TodoItem)
def get_todo(todo_id: int) -> TodoItem:

    alltodos = getData(FILE_NAME)
    for todo in alltodos:
        if TodoItem.model_validate(todo).todo_id == todo_id:
            return todo

    raise HTTPException(404, "Todo not found!")


# ----------------------------- fetch all todos -------------------------------------
# get endpoint for all endpoints with query parameter
# the query parameters are sent as strings we have to convert to int
# it uses pydantic for data validation meaning the string will be convereted to int as specified in the function defintion if possible else error will be out...
@api.get("/todos", response_model=List[TodoItem])
def get_todos(first_n: Optional[int] = None):
    alltodos = getData(FILE_NAME)
    if first_n:
        return alltodos[:first_n]
    else:
        return alltodos


# ----------------------------- Create a todo -------------------------------------
# we wantedly defined the parameters as dict. we should actually define a proper schema (id, name, description, completed) -> This is our schema but... we haven't defined it here wantedly....
@api.post("/todos", response_model=TodoItem)
def createtodos(todo: TodoCreate) -> TodoItem:
    alltodos = getData("test_backend_todolist.json")
    new_todo_id = (
        max([TodoItem.model_validate(to).todo_id for to in alltodos], default=0) + 1
    )  # this is a list comprehension given to max function directly in a single line

    new_todo = TodoItem(
        todo_id=new_todo_id,
        todo_name=todo.todo_name,
        todo_description=todo.todo_description,
        pri=todo.pri,
        completed=todo.completed,
    )

    alltodos.append(new_todo.model_dump())
    sendData(FILE_NAME, alltodos)
    return new_todo


# ----------------------------- update a todo -------------------------------------
@api.put("/todos/{todo_id}", response_model=TodoItem)
def updatetodo(todo_id: int, updated_todo: TodoUpdate) -> TodoItem | str:

    alltodos = getData(FILE_NAME)
    for index, todo in enumerate(alltodos):
        todo = TodoItem.model_validate(todo)
        if todo.todo_id == todo_id:
            todo.todo_name = updated_todo.todo_name
            todo.todo_description = updated_todo.todo_description
            todo.pri = updated_todo.pri
            todo.completed = updated_todo.completed

            alltodos[index] = todo.model_dump()
            sendData(FILE_NAME, alltodos)
            return todo

    raise HTTPException(404, "Todo not found!")


# ----------------------------- delete a todo -------------------------------------
@api.delete("/todos/{todo_id}", response_model=TodoItem)
def deletetodo(todo_id: int):
    alltodos = getData(FILE_NAME)
    for index, todo in enumerate(alltodos):
        todo = TodoItem.model_validate(todo)
        if todo.todo_id == todo_id:
            deleted_todo = alltodos.pop(index)
            sendData(FILE_NAME, alltodos)  # <-- Added this
            return deleted_todo

    raise HTTPException(404, "Todo not found!")
