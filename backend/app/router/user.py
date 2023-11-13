from typing import List
from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session
from fastapi.security import OAuth2PasswordRequestForm

from app.database.database import get_db
from app.auth.security import SecurityUtils
from app.queries.queries import Queries
from app.schema.url import ShortUrlResponse, URLAccessLogResponse


user_router = APIRouter()
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")


user_router = APIRouter()

@user_router.get("/get-all-urls", response_model=List[ShortUrlResponse])
def get_urls_for_user(current_user: dict = Depends(SecurityUtils.verify_token), db: Session = Depends(get_db)):
    
    if not current_user.get("sub"):
        raise HTTPException(status_code=404, detail="User not found")
    
    queries = Queries(db)
    all_urls = queries.get_urls_by_user_id(current_user.get("sub"))
    
    if all_urls is None:
        raise HTTPException(status_code=404, detail="URLS not found")
    
    urls_schema = [ShortUrlResponse.from_orm(url) for url in all_urls]
    
    for url in urls_schema:
        url.short_code = f"http://127.0.0.1:8000/url-shortener/redirect/{url.short_code}"
    return urls_schema



@user_router.get("/get-url-details/{url_id}", response_model=List[URLAccessLogResponse])
def get_url_details(url_id: int, current_user: dict = Depends(SecurityUtils.verify_token), db: Session = Depends(get_db)):
    queries = Queries(db)
    url_details = queries.get_url_details_by_id(url_id=url_id)

    if url_details is None:
        raise HTTPException(status_code=404, detail="URL details not found")
    
    url_details_schema = [URLAccessLogResponse.from_orm(url_detail) for url_detail in url_details]

    return url_details_schema    

