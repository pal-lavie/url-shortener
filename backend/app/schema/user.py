import re
from datetime import datetime
from typing import Optional

from pydantic import BaseModel, ConstrainedStr, EmailStr


class ConstrainedUsername(ConstrainedStr):
    min_length = 3
    max_length = 64
    regex = re.compile(r"^[A-Za-z0-9-_.]+$")
    to_lower = True
    strip_whitespace = True


# Shared properties between user models
class UserBase(BaseModel):
    username: Optional[str] = None
    email: Optional[EmailStr] = None
    is_active: bool = True
    is_superuser: bool = False


# Properties to receive on user creation
class UserRequest(BaseModel):
    username: ConstrainedUsername
    email: EmailStr
    password: str
    

class UserSchema(BaseModel):
    username: ConstrainedUsername
    email: EmailStr
    hashed_password: str


# Properties to receive on user update
class UserUpdate(UserBase):
    password: Optional[str] = None
