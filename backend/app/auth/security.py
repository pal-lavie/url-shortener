
import logging
from typing import Optional, cast, Dict, Any


from fastapi import Depends, HTTPException, status
from sqlalchemy.orm import Session
from datetime import datetime, timedelta
from hashlib import md5
from typing import Any, Optional, Union
from jose import jwt, JWTError
from passlib.context import CryptContext
from fastapi.security import OAuth2PasswordBearer


from app.config.config import settings
from app.models.user import User
from app.database.database import get_db
from app.queries.queries import Queries

logging.basicConfig(level=logging.DEBUG)
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# Algorithm used to generate the JWT token
ALGORITHM = "HS256"
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

class SecurityUtils:

    @staticmethod
    def verify_password(plain_password: str, hashed_password: str) -> bool:
        """Verify a hashed password and a plain password."""
        return pwd_context.verify(plain_password, hashed_password)

    @staticmethod
    def get_password_hash(password: str) -> str:
        """Hash a password for storing."""
        return pwd_context.hash(password)

    @staticmethod
    def authenticate_user(username: str, password: str, db: Session = Depends(get_db)):
        queries = Queries(db)
        user = queries.get_user_by_username(username)

        if not user or not SecurityUtils.verify_password(password, user.hashed_password):
            return None
        return user

    @staticmethod
    def create_access_token(
        subject: Union[str, Any],
        expires_delta: Optional[timedelta] = None,
    ) -> str:
        """Create a JWT access token."""
        if expires_delta:
            expire = datetime.utcnow() + expires_delta
        else:
            expire = datetime.utcnow() + timedelta(
                settings.ACCESS_TOKEN_EXPIRE_MINUTES,
            )
        payload = {
            "exp": expire,
            "sub": str(subject),
        }
        return jwt.encode(payload, settings.SECRET_KEY, algorithm=ALGORITHM)

    @staticmethod
    def verify_token(token: str = Depends(oauth2_scheme)) -> Dict[str, Any]:
    
        credentials_exception = HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Could not validate credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )

        try:
            payload = jwt.decode(token, settings.SECRET_KEY, algorithms=[ALGORITHM])
            
        except JWTError as e:
            logging.error(f"JWT EXCEPTION: {e}")
            raise credentials_exception
           

        return payload