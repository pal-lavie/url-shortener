# models.py

from sqlalchemy import Column, String, Integer, Boolean, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func

from app.database.database import Base

class ShortURL(Base):
    __tablename__ = 'short_urls'
    __table_args__ = {"schema": "url"}
    
    id = Column(Integer, primary_key=True, index=True)
    original_url = Column(String(600), index=True)
    short_code = Column(String(600), unique=True, index=True)
    url_use_limit = Column(Boolean, default=False)
    remaining_uses = Column(Integer, nullable=True)
    is_active = Column(Boolean, default=True)
    views = Column(Integer, default=0)
    expiry = Column(DateTime, nullable=True)
    created_at = Column(DateTime, default=func.now())
    
    user_id = Column(Integer, ForeignKey('url.users.id'))
    user = relationship('User', back_populates='short_urls')  
    short_url_access_log = relationship('ShortURLAccessLog', back_populates='short_url') 

class ShortURLAccessLog(Base):
    __tablename__ = 'short_url_access_log'
    __table_args__ = {"schema": "url"}
    
    id = Column(Integer, primary_key=True, index=True)
    ip_address = Column(String(15), index=True)
    user_agent = Column(String(200))
    access_time = Column(DateTime, server_default=func.now())
    
    short_url_id = Column(Integer, ForeignKey('url.short_urls.id'))
    short_url = relationship('ShortURL', back_populates='short_url_access_log')  