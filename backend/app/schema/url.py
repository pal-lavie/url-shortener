from datetime import datetime
from typing import Optional

from pydantic import  BaseModel


class ShortUrlRequest(BaseModel):
    original_url: str
    remaining_uses: Optional[int]
    expiry: Optional[datetime]
  

class ShortUrlResponse(BaseModel):
    id: int
    original_url: str
    short_code: str
    remaining_uses: Optional[int]
    url_use_limit: Optional[bool]
    expiry: Optional[datetime]
    is_active: Optional[bool] 
    views: Optional[int]
    created_at: Optional[datetime]
    user_id: int
    
    class Config:
        orm_mode = True
        allow_population_by_field_name = True

class URLAccessLogResponse(BaseModel):
    id: int
    ip_address: str
    user_agent: str
    access_time: datetime
    
    class Config:
        orm_mode = True
        allow_population_by_field_name = True