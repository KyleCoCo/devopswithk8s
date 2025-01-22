# Use an official Python runtime as a parent image
FROM python:3.9-slim

WORKDIR /usr/src/app


COPY . .



# Install any needed dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Set the environment variable to disable output buffering
ENV PYTHONUNBUFFERED=1

# Expose port 8000 for FastAPI
EXPOSE 8000

CMD ["python3", "-u", "read_log.py"]
