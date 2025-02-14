import asyncio
from fastapi import FastAPI
from fastapi.responses import JSONResponse
import uvicorn
import os
from counter import get_next_counter, reset_sequence


app = FastAPI()


@app.get("/pingpong")
async def pingpong():
    try:
        count = get_next_counter()
        # Return the status as JSON
        return f"pong {count}"
    except Exception as e:
        return f"Error: {e}"


@app.get("/reset_pingpong")
async def reset():
    reset_sequence(0)
    # Return the status as JSON
    return JSONResponse(content={
        "success": True
    })


def start_fastapi():
    """Start the FastAPI HTTP server."""
    uvicorn.run(app, host="0.0.0.0", port=8000)


if __name__ == "__main__":
    start_fastapi()

