import docker
import logging
from fastapi import FastAPI, Depends, HTTPException, APIRouter
from fastapi.security import APIKeyHeader


DOCKER_IMAGE_BACKEND = "localhost:5000/url-shortener-backend"
DOCKER_CONTAINER_BACKEND = "url-shortener-backend-1"
DOCKER_CONTAINER_BACKEND_PORT = "8000"
api_key = "your-secret-api-key" 
api_key_header = APIKeyHeader(name="X-API-Key")
docker_client = docker.from_env()

app = FastAPI()

def redeploy_container():
    # Pull the latest Docker image
    docker_client.images.pull(DOCKER_IMAGE_BACKEND)
    
    container_name = DOCKER_CONTAINER_BACKEND
    # Stop the existing container
    try:
        existing_container = docker_client.containers.get(container_name)
        existing_container.stop()
        existing_container.remove()
    except docker.errors.NotFound:
        pass 
    
    # Start a new container with the updated image
    docker_client.containers.run(
        DOCKER_IMAGE_BACKEND,
        name=container_name,
        detach=True,
        ports={DOCKER_CONTAINER_BACKEND_PORT: DOCKER_CONTAINER_BACKEND_PORT}
    )
    logging.info(f"Starting a new container {container_name} with updated image {DOCKER_IMAGE_BACKEND}")

@app.get("/redeploy")
def redeploy():
    if api_key == api_key:
        redeploy_container()
        return {"message": "Redeployment triggered successfully"}
    else:
        raise HTTPException(status_code=401, detail="Invalid API key")
