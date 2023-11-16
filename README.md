# URL shortener with FastAPI and React JS
A simple URL shortener with FastAPI
> allows you to provide usage limit for URLs.
> allows you to set expiry for URLs.
> shows a summary of URL access logs.

## Technologies used:
![image](https://img.shields.io/badge/Python-FFD43B?style=for-the-badge&logo=python&logoColor=blue)
![image](https://img.shields.io/badge/fastapi-109989?style=for-the-badge&logo=FASTAPI&logoColor=white)
![image](https://img.shields.io/badge/Docker-2CA5E0?style=for-the-badge&logo=docker&logoColor=white)
![image](https://img.shields.io/badge/MySQL-005C84?style=for-the-badge&logo=mysql&logoColor=white)
![image](https://img.shields.io/badge/-ReactJs-61DAFB?logo=react&logoColor=white&style=for-the-badge)

# How to Run?
You can run this project manually or by using docker-compose.

## Manually
```bash
# clone the project
git clone https://github.com/pal-lavie/url-shortener.git

cd url-shortener/backend

# install libs
pip install pipenv
pipenv install 
pipenv install --dev # for dev dependencies

# run the projct
uvicorn main:app --host 0.0.0.0 --port 8000
```

## Using docker-compose
```bash
# clone the project
git clone https://github.com/pal-lavie/url-shortener.git

# Run and build project
docker-compose build 
docker-compose up -d

```


## Using docker 
```bash
# clone the project
git clone https://github.com/pal-lavie/url-shortener.git

cd url-shortener/backend

# building docker image
docker build -t fast-api-backend .

# run the project on 8080 port
docker run -d -p 8080:8080 fast-api-backend
```

# Run the client-side React app
```bash
    $ cd client
    $ npm install
    $ npm run dev
```
