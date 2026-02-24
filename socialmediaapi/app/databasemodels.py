from sqlmodel import Field, SQLModel
from typing import Optional

class Post(SQLModel, table=True): 
    
    id: Optional[int] = Field(default=None, primary_key=True)
    title: str = Field(nullable=False)
    contents: str = Field(nullable=False)
    published: bool = Field(default=False)