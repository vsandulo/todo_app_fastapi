from pydantic import BaseModel

class User(BaseModel):
    name: str
    email: str
    password: str



class ShowUser(BaseModel):
    name: str
    email: str
    class Config():
        orm_mode = True


class Todo(BaseModel):
    title: str
    body: str

class ShowTodo(BaseModel):
    title: str
    body:str
    user_id: ShowUser
    class Config():
        orm_mode = True

