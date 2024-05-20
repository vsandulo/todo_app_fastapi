from fastapi import FastAPI
from typing import Optional
from pydantic import BaseModel

app = FastAPI()


@app.get('/todos')
def index(limit=10, completed: bool = True, sort: Optional[str] = None):
    if completed:
        return {"data": f'{limit} completed todos'}
    else:
        return {"data" : f'{limit} completed todos' }


@app.get('/todos/{id}')
def show(id: int):
    return {"data" : id}

@app.get('/todos/{id}/tasks')
def tasks(id: int):
    return {"data" : {'1', '2'}}


class Todo(BaseModel):
    title: str
    body: str
    completed: Optional[bool]



@app.post('/todos')
def create_todo(request: Todo):
    return {'data': f"Todo is created with title {request.title}"}

