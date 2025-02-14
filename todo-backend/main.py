from fastapi import FastAPI, Request
import os
import requests
from datetime import datetime, timedelta
import shutil
import uvicorn
from pydantic import BaseModel
from todo_db import insert_todo, get_all_todos


import uvicorn

app = FastAPI()

@app.on_event("startup")
async def startup_event():
    print(f"Server started on port 8000")


class TodoItem(BaseModel):
    todo: str

@app.get("/todos")
async def get_todos():
    try:
        """Return a list of todos."""
        print(get_all_todos())
        return {"todos": list(get_all_todos())}
    except Exception as e:
        print(f"Error get_todos: {e}")

@app.post("/add_todo")
async def add_todo(request: Request, item: TodoItem):
    try:
        """Add a todo to the list."""
        if len(item.todo) > 140:
            return {"error": "Todo cannot exceed 140 characters"}
        # request.client.host
        operator = request.headers.get("host")
        content = item.todo
        insert_todo(operator, content)
        return {"todos": get_all_todos()}
    except Exception as e:
        print(f"Error add_todo: {e}")


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)


