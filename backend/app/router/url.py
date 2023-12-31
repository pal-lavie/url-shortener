import logging
import pytz
import aioredis
from datetime import datetime
from fastapi import APIRouter, Depends, HTTPException, status, Request
from fastapi.responses import RedirectResponse
from sqlalchemy.orm import Session

from app.auth.security import SecurityUtils
from app.database.database import get_db
from app.schema.url import ShortUrlResponse, ShortUrlRequest
from app.schema.user import UserBase
from app.utils.short_url_generator import url_generator
from app.queries.queries import Queries
from app.models.url import ShortURL, ShortURLAccessLog
from app.utils.date_utils import get_created_at

logging.basicConfig(level=logging.DEBUG)


url_router = APIRouter()


async def create_redis_pool():
    return await aioredis.from_url('redis://localhost:6379/0')

async def acquire_lock(redis, key):
    lock = await redis.lock(key, timeout=10)
    await lock.acquire()
    return lock

async def release_lock(lock):
    await lock.release()


def is_url_expired(metadata: ShortURL) -> bool:
    if metadata.expiry:
        return get_created_at() > metadata.expiry.astimezone(pytz.utc)
    return False

def is_url_usage_limit_active(metadata: ShortURL):
    if metadata.url_use_limit:
        if metadata.remaining_uses == 0:
            return False
    return True

@url_router.post("/create-short-url", response_model=ShortUrlResponse)
def create_short_url(payload: ShortUrlRequest, db: Session = Depends(get_db), current_user: dict = Depends(SecurityUtils.verify_token)):
    shortened_url = url_generator.generate_unique_short_url(payload.original_url, db)
    query = Queries(db)
    user = query.get_user_by_id(int(current_user.get("sub")))
    
    url_use_limit = False
    if payload.remaining_uses and payload.remaining_uses > 0:
        url_use_limit = True
    short_url_object = ShortURL(
        original_url=payload.original_url,
        short_code=shortened_url,
        remaining_uses=payload.remaining_uses,
        expiry=payload.expiry,
        url_use_limit=url_use_limit,
        user=user,
        created_at=get_created_at(),
    )
    # create short code 
    short_url_response = query.create_short_url(short_url_object)
    shortened_url = f"http://127.0.0.1:8000/url-shortener/redirect/{short_url_response.short_code}"
    
    return ShortUrlResponse(
        id=short_url_response.id,
        user_id=short_url_object.user_id,
        original_url=short_url_response.original_url,
        short_code=shortened_url,
        user=UserBase(
            username=user.username,
            email=user.email,
            is_active=user.is_active,
            is_superuser=user.is_superuser),
        remaining_uses=short_url_response.remaining_uses,
        expiry=short_url_response.expiry,
        is_active=short_url_response.is_active,
        views=short_url_response.views,
        created_at=short_url_response.created_at,
    )    


@url_router.get("/redirect/{short_code}", response_class=RedirectResponse)
async def redirect_to_original_url(short_code: str, request: Request, db: Session = Depends(get_db)):
    # Look up the short code in the mapping
    queries = Queries(db)
    url_obj = queries.get_url_by_short_code(short_code)
    if url_obj is None:
        # If the short code is not found, return a 404 Not Found response
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Short code not found")
    
     # Get the client's IP address
    client_ip = request.client.host
    # Get the user-agent
    user_agent = request.headers.get("user-agent")
    
    access_log = ShortURLAccessLog(
            ip_address=client_ip,
            user_agent=user_agent,
            access_time=get_created_at(),
            short_url=url_obj,
        )
    
    # Add access log data
    queries.add_url_access_log(acess_log=access_log)

    
    if is_url_expired(url_obj):
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="URL has expired")
    
    if not is_url_usage_limit_active(url_obj):
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="URL usage limit has expired")
    
   
        
    if url_obj.url_use_limit and url_obj.remaining_uses > 0:
        redis = await create_redis_pool()
        lock_key = f"short_url_lock:{short_code}"
        lock =  acquire_lock(redis, lock_key)
        try:
            
            url_obj = queries.update_url_use_count(short_url=short_code, usage_count=url_obj.remaining_uses-1)    
            
        finally:
            release_lock(lock)
              
    # Perform the redirection
    return RedirectResponse(url=url_obj.original_url)
        
