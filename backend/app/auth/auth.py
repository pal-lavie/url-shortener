import logging
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from fastapi.responses import ORJSONResponse, JSONResponse
from fastapi.security import OAuth2PasswordRequestForm
from datetime import timedelta



from app.config.config import settings
from app.database.database import get_db
from app.schema.user import UserRequest
from app.schema.token import AuthToken
from app.queries.queries import Queries
from app.auth.security import SecurityUtils
from app.models.user import User


logging.basicConfig(level=logging.DEBUG)

auth_router = APIRouter(
    responses={
        401: {
            "description": "Unauthorized, invalid credentials or access token",
        },
    },
)

@auth_router.post("/sign-up", response_model=None)
def create_user(user_request: UserRequest, db: Session = Depends(get_db)):
    logging.info(f"create user flow started")
    queries = Queries(db)
    db_user_email = queries.get_user_by_email(user_request.email)
    db_user_name = queries.get_user_by_username(user_request.username)
    if db_user_email or db_user_name:
        raise HTTPException(status_code=400, detail="Email/Username already registered")
    user = User(
        username=user_request.username,
        email=user_request.email,
        hashed_password=SecurityUtils.get_password_hash(user_request.password)
    )
    logging.info(f"user created successfully")
    queries.create_user(user=user)
    return JSONResponse(content={"message": "User created successfully"}, status_code=201)

@auth_router.post(
    "/access-token",
    response_model=AuthToken
)
def generate_access_token(
    form_data: OAuth2PasswordRequestForm = Depends(),
     db: Session = Depends(get_db),
) -> ORJSONResponse:
    """Get an access token for future requests."""
    logging.info(f"Acces-token user flow started")
    user = SecurityUtils.authenticate_user(
        username=form_data.username,
        password=form_data.password,
        db=db,
    )
    if not user:
    
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
        )
    elif not user.is_active:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Inactive user",
        )
    expires_in = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    return ORJSONResponse(
        content={
            "access_token": SecurityUtils.create_access_token(
                user.id,
                expires_delta=expires_in,
            ),
            "token_type": "bearer",
        },
    )
    
@auth_router.post(
        "/api-key",
        response_model=str,
        status_code=status.HTTP_201_CREATED,
        
    )
def generate_new_api_key(self, current_user: dict = Depends(SecurityUtils.verify_token)) -> User:
    """Create a new API key for current user."""
    return  SecurityUtils.create_api_key()
