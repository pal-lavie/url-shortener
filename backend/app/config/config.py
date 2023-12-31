import secrets
from pydantic import BaseSettings


class Settings(BaseSettings):
    APP_NAME: str = "url shortener"
    APP_VERSION: str = "v1"
    DEBUG: bool = True
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60 * 24 * 1  # 60 minutes * 24 hours * 1 = 1 day
    SECRET_KEY: str = secrets.token_urlsafe(32)
    DATABASE_URL: str = "mysql+pymysql://user:pass@mysql:3306"

    DOCKER_IMAGE_BACKEND = "url-shortener-backend"
    DOCKER_CONTAINER_BACKEND = "url-shortener-backend-1"
    DOCKER_CONTAINER_BACKEND_PORT = "8000"
settings = Settings()