from pydantic import BaseModel


class Todo(BaseModel):
    title: str
    body: str