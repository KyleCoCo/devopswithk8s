from fastapi import FastAPI
import os
import requests
from datetime import datetime, timedelta
import shutil
import uvicorn
from pydantic import BaseModel


import uvicorn

app = FastAPI()

@app.on_event("startup")
async def startup_event():
    print(f"Server started on port 8000")


# In-memory "database" for todos
todos = ["TODO 1", "TODO 2"]

class TodoItem(BaseModel):
    todo: str

@app.get("/todos")
async def get_todos():
    """Return a list of todos."""
    return {"todos": todos}

@app.post("/add_todo")
async def add_todo(item: TodoItem):
    """Add a todo to the list."""
    if len(item.todo) > 140:
        return {"error": "Todo cannot exceed 140 characters"}
    todos.append(item.todo)
    return {"todos": todos}

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)


