from enum import IntEnum
from typing import List, Optional
from data import getData, sendData
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field
from backend.models import Priority, TodoCreate, TodoItem, TodoUpdate


FILE_NAME = "test_backend_todolist.json"

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

def get_todo(todo_id: int) -> TodoItem:

    alltodos = getData(FILE_NAME)
    for todo in alltodos:
        if TodoItem.model_validate(todo).todo_id == todo_id:
            return todo

    raise HTTPException(404, "Todo not found!")


def get_todos(first_n: Optional[int] = None):
    alltodos = getData(FILE_NAME)
    if first_n:
        return alltodos[:first_n]
    else:
        return alltodos


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


def deletetodo(todo_id: int):
    alltodos = getData(FILE_NAME)
    for index, todo in enumerate(alltodos):
        todo = TodoItem.model_validate(todo)
        if todo.todo_id == todo_id:
            deleted_todo = alltodos.pop(index)
            sendData(FILE_NAME, alltodos)  # <-- Added this
            return deleted_todo

    raise HTTPException(404, "Todo not found!")
