from sqlalchemy import Column, Integer, String, DateTime, func, Boolean
from sqlalchemy.orm import relationship

from app.database.database import Base

# SQLAlchemy Model
class User(Base):
    __tablename__ = 'users'
    __table_args__ = {"schema": "url"}
    
    id = Column(Integer, primary_key=True, index=True)
    username = Column(String(100), unique=True, index=True)
    email = Column(String(100), unique=True, index=True)
    hashed_password = Column(String(100))
    is_active = Column(Boolean, default=True)
    is_superuser = Column(Boolean, default=False)
    created_at = Column(DateTime, default=func.now())
   
    short_urls = relationship('ShortURL', back_populates='user')