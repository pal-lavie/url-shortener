#!/bin/bash

# Stop the existing Docker container
docker stop url-shortener-backend

# Remove the existing Docker container
docker rm url-shortener-backend

# Pull the latest Docker image
docker pull url-shortener-backend/your_image:latest

# Start a new Docker container
docker run -d --name url-shortener-backend -p 80:80 your_registry/url-shortener-backend:latest
