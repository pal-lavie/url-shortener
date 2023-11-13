import logging
import pytz
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
from app.utils.date_utils import get_created_at, get_datetime_now

logging.basicConfig(level=logging.DEBUG)


url_router = APIRouter()


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

def is_url_expired(metadata: ShortURL) -> bool:
    if metadata.expiry:
        return get_created_at() > metadata.expiry.astimezone(pytz.utc)
    return False

def is_url_usage_limit_active(metadata: ShortURL):
    if metadata.url_use_limit:
        if metadata.remaining_uses == 0:
            return False
    return True
    


@url_router.get("/redirect/{short_code}", response_class=RedirectResponse)
def redirect_to_original_url(short_code: str, request: Request, db: Session = Depends(get_db)):
    # Look up the short code in the mapping
    queries = Queries(db)
    url_obj = queries.get_url_by_short_code(short_code)
    if url_obj is None:
        # If the short code is not found, return a 404 Not Found response
        raise HTTPException(status_code=404, detail="Short code not found")
    
    if is_url_expired(url_obj):
        raise HTTPException(status_code=410, detail="URL has expired")
    
    if not is_url_usage_limit_active(url_obj):
        raise HTTPException(status_code=410, detail="URL usage limit has expired")
    
    if url_obj:
        if url_obj.url_use_limit:
            if url_obj.remaining_uses > 0:
                url_obj = queries.update_url_use_count(short_url=short_code, usage_count=url_obj.remaining_uses-1)
    
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
    
    # Perform the redirection
    return RedirectResponse(url=url_obj.original_url)