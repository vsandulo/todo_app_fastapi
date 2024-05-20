from fastapi import FastAPI, Depends, status, HTTPException, Response
from . import schemas, models
from .database import engine, SessionLocal
from sqlalchemy.orm import Session



app = FastAPI()

models.Base.metadata.create_all(engine)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@app.post('/todo', status_code=status.HTTP_201_CREATED)
def create(request: schemas.Todo, db: Session = Depends(get_db)):
    new_todo = models.Todo(title=request.title, body=request.body)
    db.add(new_todo)
    db.commit()
    db.refresh(new_todo)
    return new_todo
 

@app.get('/todo')
def index(db: Session = Depends(get_db)):
    todos = db.query(models.Todo).all()
    return todos


@app.get('/todo/{id}', status_code=status.HTTP_200_OK)
def show(id, response: Response, db: Session = Depends(get_db)):
    todo = db.query(models.Todo).filter(models.Todo.id == id).first()
    if not todo:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"Todo with the id {id} is not available")
    response.status_code = status.HTTP_404_NOT_FOUND
    return todo

@app.delete('/todo/{id}', status_code=status.HTTP_204_NO_CONTENT)
def destroy(id, db: Session = Depends(get_db)):
    todo = db.query(models.Todo).filter(models.Todo.id == id) 
 
    if not todo.first():
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"Todo with id {id} not found")

    todo.delete(synchronize_session=False)
    db.commit()
    return 'done'


@app.put('/todo/{id}', status_code=status.HTTP_202_ACCEPTED)
def update(id: int, request: schemas.Todo, db: Session = Depends(get_db)):
    todo = db.query(models.Todo).filter(models.Todo.id == id).first()

    if not todo:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"Todo with id {id} not found")

    todo_data = request.dict(exclude_unset=True)
    for key, value in todo_data.items():
        setattr(todo, key, value)
    
    db.commit()
    return 'updated'

