import requests
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
# PINGPONG_GET = "http://127.0.0.1:8081/pingpong"
PINGPONG_GET = "http://ping-pong-svc:2348/pingpong"
INFORMATION_FILE = "/etc/foo/information.txt"

@app.get("/status")
async def get_status():
    try: 
        global random_string
        current_time = get_current_time() 
        pingpong_count = ""
        # Read content from a pod
        response = requests.get(PINGPONG_GET, stream=True)
        if response.status_code == 200:
            pingpong_count = response.content.decode()
        pingpong_count = pingpong_count[6:]
        information_content = ""
        # Read content from a file
        with open(INFORMATION_FILE, 'r') as file:
            information_content = file.read()
        return "file content: this text is from file\nenv variable: " + \
                information_content + "\n" + \
                get_out_put(current_time) + ".\n" + \
                "Ping / Pongs: " + pingpong_count
    except Exception as e:
        return JSONResponse(content={
            "error": str(e)
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
        return JSONResponse(content={
            "error": str(e)
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


def get_out_put(current_time):
    global random_string
    return f"{current_time}: {random_string}"


def log_output():
    try: 
        # Output the random string every 5 seconds with a timestamp
        while True:
            # Get the current time in ISO 8601 format with milliseconds
            current_time = get_current_time() 
            # Print the timestamp and random string
            content = get_out_put(current_time)          
            print(content)
            # Open the file in write mode ('w') or append mode ('a') if you don't want to overwrite
            with open(log_file, 'a') as file:
                file.write(f"{content}\n")
            # Wait for 5 seconds
            time.sleep(5)
    except Exception as e:
        print(f"Error occurred: {e}")


def start_fastapi():
    """Start the FastAPI HTTP server."""
    uvicorn.run(app, host="0.0.0.0", port=8000)


# @app.on_event("startup")
# async def startup_event():
#     print("Starting periodic task thread...")
#     thread.start()  # Start the background thread when the app starts


if __name__ == "__main__":
    random_string = generate_random_string()
    # Start the periodic task in a separate thread
    thread = threading.Thread(target=log_output, daemon=True)
    thread.start()
    # Start FastAPI in the main thread
    start_fastapi()

