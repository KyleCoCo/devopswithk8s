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

random_string = ""

def generate_random_string():
    """Generates a random UUID-style string."""
    return str(uuid.uuid4())


def get_current_time():
    current_time = datetime.datetime.now(datetime.timezone.utc).strftime("%Y-%m-%dT%H:%M:%S.") + f"{int(time.time() * 1000) % 1000:03d}Z"
    return current_time


def get_out_put(current_time):
    global random_string
    return f"{current_time}: {random_string}"


async def log_output():
    try: 
        # Output the random string every 5 seconds with a timestamp
        while True:
            # Get the current time in ISO 8601 format with milliseconds
            current_time = get_current_time() 
            # Print the timestamp and random string
            print(get_out_put(current_time))            
        
            # Wait for 5 seconds
            await asyncio.sleep(5)
    except Exception as e:
        print(f"Error occurred: {e}")


def start_fastapi():
    """Start the FastAPI HTTP server."""
    uvicorn.run(app, host="0.0.0.0", port=8000)


if __name__ == "__main__":
    random_string = generate_random_string()
    # Create an event loop for the background task
    loop = asyncio.get_event_loop()

    # Start the logging function in the background (non-blocking)
    loop.create_task(log_output())
    
    # Start FastAPI in the main thread
    start_fastapi()

