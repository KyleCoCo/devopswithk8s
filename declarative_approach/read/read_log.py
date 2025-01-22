import random
import string
import time
import datetime
import uuid
import threading
import asyncio
from fastapi import FastAPI
from fastapi.responses import JSONResponse
import uvicorn
import os

app = FastAPI()

@app.get("/status")
async def get_status():
    global random_string
    current_time = get_current_time() 
    # Return the status as JSON
    return JSONResponse(content={
        "timestamp": current_time,
        "random_string": random_string
    })


@app.get("/readlog")
async def read_log():
    try:
        global random_string
        current_time = get_current_time() 
        log_content = ""
        # Read content from a file
        with open(log_file, 'r') as file:
            log_content = file.read()
        
        # Return the status as JSON
        return JSONResponse(content={
            "timestamp": current_time,
            "random_string": random_string,
            "log_content": log_content
        })
    except Exception as e:
        JSONResponse(content={
            "error": e
        })

random_string = ""
log_file = "/usr/log/log.txt"
# Create any missing directories
os.makedirs(os.path.dirname(log_file), exist_ok=True)

def generate_random_string():
    """Generates a random UUID-style string."""
    return str(uuid.uuid4())


def get_current_time():
    current_time = datetime.datetime.now(datetime.timezone.utc).strftime("%Y-%m-%dT%H:%M:%S.") + f"{int(time.time() * 1000) % 1000:03d}Z"
    return current_time


def start_fastapi():
    """Start the FastAPI HTTP server."""
    uvicorn.run(app, host="0.0.0.0", port=8000)


if __name__ == "__main__":
    random_string = generate_random_string()
    # Start FastAPI in the main thread
    start_fastapi()

