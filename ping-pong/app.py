import asyncio
from fastapi import FastAPI
from fastapi.responses import JSONResponse
import uvicorn

app = FastAPI()

pingpong_count = 0

@app.get("/pingpong")
async def pingpong():
    global pingpong_count
    count = pingpong_count
    pingpong_count += 1
    # Return the status as JSON
    return f"pong {count}"


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

