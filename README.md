
# Todo App FastAPI

  

This project is an example of using FastAPI to create a RESTful API for managing tasks (todos) and users.
and maybe need to add sub-task or other

  

## Requirements

  

Before running the project, you need to install the necessary dependencies:

  

```
pip3  install  -r  requirements.txt
```



## Running the Project

To  run  the  project  locally,  use  the  following  command.  This  will  start  the  server  on  localhost  at  port  8000:

  

```
uvicorn todo.main:app --reload
```

After starting the server, you can open your browser and go to http://localhost:8000/ to view the API documentation automatically generated by Swagger UI.

  

## Running Tests

To run the tests, ensure you are in the root directory of the project. Use the following command to execute the tests:

  
```
pytest
```
