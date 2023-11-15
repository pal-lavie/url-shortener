# Use an official Python runtime as a parent image
FROM python:3.9

# Set the working directory to /app
WORKDIR /app

# Copy the current directory contents into the container at /app
COPY . /app


# Install system dependencies
RUN apt-get update \
    && apt-get install -y --no-install-recommends build-essential \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

# Install pipenv
RUN pip install docker
RUN pip install fastapi
RUN pip install uvicorn


# Make port 8000 available to the world outside this container
EXPOSE 8080

# Run the application
CMD ["uvicorn",  "app.main:app", "--host", "0.0.0.0", "--port", "8080"]
