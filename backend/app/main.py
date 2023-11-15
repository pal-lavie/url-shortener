from fastapi import FastAPI, Depends
from fastapi import Depends, FastAPI
from fastapi.middleware.cors import CORSMiddleware


from app.auth.auth import auth_router
from app.router.url import url_router
from app.router.user import user_router
from app.config.config import settings
from app.auth.security import SecurityUtils
from app.models.user import User
# from app.database.database import engine, get_db

URL_PREFIX = "/url-shortener"
app = FastAPI(
    debug=settings.DEBUG,
    title=settings.APP_NAME,
    version=settings.APP_VERSION,
)
app.include_router(auth_router, prefix=URL_PREFIX, tags=["user-auth"])
app.include_router(url_router, prefix=URL_PREFIX, tags=["create-short-url"])
app.include_router(user_router, prefix=URL_PREFIX,tags=["get-user-urls"])

# Enable CORS for all origins
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # You should restrict this to specific domains in production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
async def root():
    return {"message": "Hello World"}

@app.get("/secure-endpoint")
def secure_endpoint(current_user: dict = Depends(SecurityUtils.verify_token)):
    return {"message": "This is a secure endpoint", "user": current_user}



