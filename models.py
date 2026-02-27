from pydantic import BaseModel
from typing import Optional 

class BasePost(BaseModel):
    title: str
    content: str
    published: bool = True
