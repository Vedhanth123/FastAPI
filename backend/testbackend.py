# THis file contains learnings from https://www.youtube.com/watch?v=rvFsGRvj9jo

# let's creata a simple todo list api
# now extending this


from data import getData, sendData
from fastapi import FastAPI

api = FastAPI()

FILE_NAME = "test_backend_todolist.json"


# GET, POST, PUT (updating), DELETE
@api.get("/")
def index():
    return {"msg": "Hey joker!"}


# We can also define sync and async endpoints.

"""
# async endopoint example (only used for IO bounds for example interacting with the database.)
@api.get('/getdata')
async def getData():
    # This isu 
"""
# creating endpoints for getting all todoes, creating, updating, deleting (basic CRUD operations)


# ----------------------------- Path parameter fetch a single todo -------------------------------------
# get endpoint
@api.get("/todos/{todo_id}")
def get_todos(todo_id: int):

    alltodos = getData(FILE_NAME)
    for todo in alltodos:
        if todo["id"] == todo_id:
            return {"result": todo}


# ----------------------------- fetch all todos -------------------------------------
# get endpoint for all endpoints with query parameter
# the query parameters are sent as strings we have to convert to int
# it uses pydantic for data validation meaning the string will be convereted to int as specified in the function defintion if possible else error will be out...
@api.get("/todos")
def get_todo(first_n: int = None):
    alltodos = getData(FILE_NAME)
    if first_n:
        return alltodos[:first_n]
    else:
        return alltodos


# ----------------------------- Create a todo -------------------------------------
@api.post("/todos")
# we wantedly defined the parameters as dict. we should actually define a proper schema (id, name, description, completed) -> This is our schema but... we haven't defined it here wantedly....
def createtodos(todo: dict):
    alltodos = getData("test_backend_todolist.json")
    new_todo_id = max(
        todo["id"] for todo in alltodos
    )  # this is a list comprehension given to max function directly in a single line

    new_todo = {
        "id": new_todo_id + 1,
        "title": todo["title"],
        "description": todo["description"],
        "completed": todo["completed"],
    }

    alltodos.append(new_todo)
    return sendData(FILE_NAME, alltodos)


# ----------------------------- update a todo -------------------------------------
@api.put("/todos/{todo_id}")
def updatetodo(todo_id: int, updated_todo: dict):

    alltodos = getData(FILE_NAME)
    new_todo = next(filter(lambda todo: todo["id"] == todo_id, alltodos))
    if(new_todo):
        new_todo['title'] = updated_todo['title']
        new_todo['description'] = updated_todo['description']
        new_todo['completed'] = updated_todo['completed']

        return sendData(FILE_NAME, alltodos)
    else:
        return False

# ----------------------------- delete a todo -------------------------------------
@api.delete("/todos/{todo_id}")
def deletetodo(todo_id: int):
    alltodos = getData(FILE_NAME)
    new_todo = next(filter(lambda todo: todo["id"] == todo_id, alltodos))

    if(new_todo):
        alltodos.remove(new_todo)
        return sendData(FILE_NAME, alltodos)
    else:
        return False