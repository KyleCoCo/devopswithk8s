import asyncio
from fastapi import FastAPI
from fastapi.responses import JSONResponse
import uvicorn
import os

app = FastAPI()
pingpong_count_file = "/usr/log/pingpong/count.txt"
os.makedirs(os.path.dirname(pingpong_count_file), exist_ok=True)


pingpong_count = 0

@app.get("/pingpong")
async def pingpong():
    try:
        global pingpong_count
        count = pingpong_count
        # Open the file in write mode ('w') or append mode ('a') if you don't want to overwrite
        with open(pingpong_count_file, 'w') as file:
            file.write(f"{count}\n")
        pingpong_count += 1
        # Return the status as JSON
        return f"pong {count}"
    except Exception as e:
        return f"Error: {e}"


@app.get("/reset_pingpong")
async def reset():
    global pingpong_count
    pingpong_count = 0
    # Return the status as JSON
    return JSONResponse(content={
        "success": True
    })


def start_fastapi():
    """Start the FastAPI HTTP server."""
    uvicorn.run(app, host="0.0.0.0", port=8000)


if __name__ == "__main__":
    start_fastapi()

