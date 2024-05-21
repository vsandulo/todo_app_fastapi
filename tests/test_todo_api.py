from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from todo.main import app
from todo.database import Base, get_db
from todo.models import Todo
import pytest

SQLALCHEMY_DATABASE_URL = "sqlite:///./test_database.db"
engine = create_engine(SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False})
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def override_get_db():
    try:
        db = TestingSessionLocal()
        yield db
    finally:
        db.close()

app.dependency_overrides[get_db] = override_get_db

client = TestClient(app)

def setup_function(function):
    Base.metadata.create_all(bind=engine)

def teardown_function(function):
    Base.metadata.drop_all(bind=engine)

def test_create_todo():
    response = client.post("/todo", json={"title": "Complete the project", "body": "Need to work on the project", "user_id": 1})
    assert response.status_code == 201
    data = response.json()
    assert data["title"] == "Complete the project"
    assert "id" in data

@pytest.mark.skip(reason="Need to fix user flow")
def test_read_todo_list():
    response = client.post("/todo", json={"title": "Complete the project", "body": "Need to work on the project", "user_id": 1})
    assert response.status_code == 201

    response = client.get("/todo")
    assert response.status_code == 200
    data = response.json()
    assert len(data) == 1
    assert data[0]["title"] == "Complete the project"

@pytest.mark.skip(reason="Need to fix user flow")
def test_read_single_todo():
    response = client.post("/todo", json={"title": "Test Todo", "body": "Test the get single todo endpoint", "user_id": 1})
    assert response.status_code == 201
    todo_id = response.json()["id"]

    response = client.get(f"/todo/{todo_id}")
    assert response.status_code == 200
    assert response.json()["title"] == "Test Todo"

def test_update_todo():
    response = client.post("/todo", json={"title": "Original Title", "body": "Original Body", "user_id": 1})
    assert response.status_code == 201
    todo_id = response.json()["id"]

    response = client.put(f"/todo/{todo_id}", json={"title": "Updated Title", "body": "Updated Body"})
    assert response.status_code == 202
    updated_data = response.json()
    assert updated_data == 'updated'

def test_delete_todo():
    response = client.post("/todo", json={"title": "To Delete", "body": "Delete this todo", "user_id": 1})
    assert response.status_code == 201
    todo_id = response.json()["id"]

    response = client.delete(f"/todo/{todo_id}")
    assert response.status_code == 204

    response = client.get(f"/todo/{todo_id}")
    assert response.status_code == 404
