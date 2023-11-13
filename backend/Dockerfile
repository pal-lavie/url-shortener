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
RUN pip install pipenv

# Install project dependencies
RUN pipenv install --deploy --ignore-pipfile

# Install Alembic dependencies
RUN pipenv install --deploy --ignore-pipfile --dev

# Download wait-for-it script
ADD https://raw.githubusercontent.com/vishnubob/wait-for-it/master/wait-for-it.sh /app/wait-for-it.sh
RUN chmod +x /app/wait-for-it.sh


# Make port 8000 available to the world outside this container
EXPOSE 8000

# Run the application
CMD ["./wait-for-it.sh", "mysql:3306", "--", "pipenv", "run", "uvicorn",  "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
