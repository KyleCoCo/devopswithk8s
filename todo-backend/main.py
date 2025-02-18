from fastapi import FastAPI, Request
import os
import logging
import requests
from datetime import datetime, timedelta
import shutil
import uvicorn
from pydantic import BaseModel
from todo_db import insert_todo, get_all_todos
from config import init_log_config
import uvicorn

init_log_config()
logger = logging.getLogger(__name__)
app = FastAPI()


@app.on_event("startup")
async def startup_event():
    logger.info(f"Server started on port 8000")


class TodoItem(BaseModel):
    todo: str

@app.get("/todos")
async def get_todos():
    try:
        """Return a list of todos."""
        return {"todos": list(get_all_todos())}
    except Exception as e:
        logger.error("Error get_todos", e)

@app.post("/add_todo")
async def add_todo(request: Request, item: TodoItem):
    try:
        """Add a todo to the list."""
        if len(item.todo) > 140:
            logger.error("Todo cannot exceed 140 characters")
            return {"error": "Todo cannot exceed 140 characters"}
        # request.client.host
        operator = request.client.host
        content = item.todo
        insert_todo(operator, content)
        return {"todos": get_all_todos()}
    except Exception as e:
        logger.error("Error add_todo", e)


if __name__ == "__main__":
    # init_log_config()
    uvicorn.run(app, host="0.0.0.0", port=8000, log_config=None)


