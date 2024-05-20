from pydantic import BaseModel


class Todo(BaseModel):
    title: str
    body: str

class ShowTodo(BaseModel):
    title: str
    body:str
    class Config():
        orm_mode = True