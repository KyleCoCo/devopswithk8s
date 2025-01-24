from fastapi import FastAPI, HTTPException
from fastapi.responses import HTMLResponse, FileResponse, JSONResponse
from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.triggers.cron import CronTrigger
import os
import requests
from datetime import datetime, timedelta
import shutil
import uvicorn
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from starlette.requests import Request
from pydantic import BaseModel


import uvicorn

app = FastAPI()

# Set up static file serving
app.mount("/static", StaticFiles(directory="static"), name="static")

# Set up Jinja2 templates
templates = Jinja2Templates(directory="templates")

# Configuration
IMAGE_DIRECTORY = "/usr/fastapi-app/images"
IMAGE_FILENAME = "photo.jpg"
IMAGE_PATH = os.path.join(IMAGE_DIRECTORY, IMAGE_FILENAME)
IMAGE_URL = "https://picsum.photos/1200"  # Replace with your image URL
REPLACE_INTERVAL_MINUTES = 60

# Ensure the image directory exists
os.makedirs(IMAGE_DIRECTORY, exist_ok=True)


@app.on_event("startup")
async def startup_event():
    download_image()
    print(f"Server started on port 8000")


@app.get("/")
def read_html(request: Request):
    # return {"message": "Hello, World!"}
    # Render the index.html template
    return templates.TemplateResponse("index.html", {"request": request})


# Function to check image's existence and age
def is_image_valid() -> bool:
    if os.path.exists(IMAGE_PATH):
        file_mod_time = datetime.fromtimestamp(os.path.getmtime(IMAGE_PATH))
        if datetime.now() - file_mod_time < timedelta(minutes=REPLACE_INTERVAL_MINUTES):
            return True
    return False


# Function to download the image
def download_image():
    print("Starting image download...")
    
    try:
        # Check if the image exists and is valid
        if is_image_valid():
            print("Image is already valid (exists and is fresh enough). Skipping download.")
            return
        
        # Fetch image from the URL
        response = requests.get(IMAGE_URL, stream=True)
        if response.status_code == 200:
            # Save the image with a new version
            with open(IMAGE_PATH, "wb") as f:
                shutil.copyfileobj(response.raw, f)
            print(f"Image downloaded and saved to: {IMAGE_PATH}")
        else:
            print(f"Failed to download image, status code: {response.status_code}")
    except Exception as e:
        print(f"Error while downloading image: {e}")


# Schedule periodic downloads using APScheduler
scheduler = BackgroundScheduler()
scheduler.add_job(download_image, CronTrigger.from_crontab("*/5 * * * *"))  # Download every 5 minutes
scheduler.start()


@app.on_event("shutdown")
def shutdown_event():
    scheduler.shutdown()


@app.post("/download")
async def download():
    """Download the image manually."""
    download_image()
    return {"message": "Image downloaded successfully!"}


@app.get("/show", response_class=HTMLResponse)
async def show_image(request: Request):
    """Show the image in an HTML response."""
    if not os.path.exists(IMAGE_PATH):
        raise HTTPException(status_code=404, detail="Image not found!")
    return templates.TemplateResponse("index.html", {"request": request})


@app.get("/photo")
async def get_photo():
    """Serve the image file."""
    if not os.path.exists(IMAGE_PATH):
        raise HTTPException(status_code=404, detail="Image not found!")
    return FileResponse(IMAGE_PATH)


@app.get("/downloaded_images/{filename}")
async def get_image(filename: str):
    """Serve the image file."""
    file_path = os.path.join(IMAGE_DIRECTORY, filename)
    if not os.path.exists(file_path):
        raise HTTPException(status_code=404, detail="Image not found!")
    return FileResponse(file_path)


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)


