import docker
import logging
from fastapi import FastAPI, Depends, HTTPException, APIRouter
from fastapi.security import APIKeyHeader

from app.config.config import settings


api_key = "your-secret-api-key" 
api_key_header = APIKeyHeader(name="X-API-Key")
docker_client = docker.from_env()

deployment_router = APIRouter()

def redeploy_container():
    # Pull the latest Docker image
    docker_client.images.pull(f"{settings.DOCKER_IMAGE_BACKEND}:latest")
    
    container_name = settings.DOCKER_CONTAINER_BACKEND
    # Stop the existing container
    try:
        existing_container = docker_client.containers.get(container_name)
        existing_container.stop()
        existing_container.remove()
    except docker.errors.NotFound:
        pass 
    
    # Start a new container with the updated image
    docker_client.containers.run(
        f"{settings.DOCKER_IMAGE_BACKEND}:latest",
        name=container_name,
        detach=True,
        ports={settings.DOCKER_CONTAINER_BACKEND_PORT: settings.DOCKER_CONTAINER_BACKEND_PORT}
    )
    logging.info(f"Starting a new container {container_name} with updated image {settings.DOCKER_IMAGE_BACKEND}")

@deployment_router.post("/redeploy")
async def redeploy():
    if api_key == api_key:
        redeploy_container()
        return {"message": "Redeployment triggered successfully"}
    else:
        raise HTTPException(status_code=401, detail="Invalid API key")
