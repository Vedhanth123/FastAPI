# THis file contains learnings from https://www.youtube.com/watch?v=rvFsGRvj9jo

# In this file we will be defining pydantic models which are like user defined datatypes which helps in data validation


from enum import IntEnum

from pydantic import BaseModel, Field


class Priority(IntEnum):
    LOW = 3
    HIGH = 1
    MEDIUM = 2


class TodoBase(BaseModel):
    todo_name: str = Field(
        ..., min_length=3, max_length=512, description="Name of the task"
    )
    todo_description: str = Field(..., description="Description of the todo")

    pri: Priority = Field(default=Priority.LOW, description="Priority of the todo")

    completed: bool = Field(default=False, description="task status")


class TodoUpdate(BaseModel):
    todo_name: str | None = Field(
        default=None, min_length=3, max_length=512, description="Name of the task"
    )
    todo_description: str | None = Field(
        default=None, description="Description of the todo"
    )

    pri: Priority | None = Field(default=None, description="Priority of the todo")
    completed: bool | None = Field(default=None, description="task status")


class TodoCreate(TodoBase):
    pass


class TodoItem(TodoBase):
    todo_id: int = Field(..., description="unique identifier of the todo")


# We are defining again because while updating we might not update everything so.. it is not same as the TodoBase
# and if you observer I've also put everything as Optional too...
