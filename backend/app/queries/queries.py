from typing import List
from sqlalchemy.orm import Session
from app.models.user import User  
from app.models.url import ShortURL, ShortURLAccessLog
import logging
logging.basicConfig(level=logging.DEBUG)

class Queries:
    def __init__(self, db: Session):
        self.db = db

    def create_user(self, user: User):
        try:
            self.db.add(user)
            self.db.commit()
            self.db.refresh(user)
            return user
        except Exception as e:
            logging.error(f"Error during database insertion: {e}")
            # Rollback the transaction on error
            self.db.rollback()
            return None

    def get_user_by_id(self, user_id: int):
        return self.db.query(User).filter(User.id == user_id).first()

    def get_user_by_username(self, username: str):
        return self.db.query(User).filter(User.username == username).first()

    def get_user_by_email(self, email: str):
        return self.db.query(User).filter(User.email == email).first()

    def get_all_users(self):
        return self.db.query(User).all()
    
    def create_short_url(self, short_url: ShortURL):
        try:
            self.db.add(short_url)
            self.db.commit()
            self.db.refresh(short_url)
            return short_url
        except Exception as e:
            logging.error(f"Error during database insertion: {e}")
            # Rollback the transaction on error
            self.db.rollback()
            return None
        
    def get_url_by_short_code(self, short_url: str):
        return self.db.query(ShortURL).filter(ShortURL.short_code == short_url).first()
    
    def update_url_use_count(self, short_url : str, usage_count: int):
        try:
            url_obj = self.db.query(ShortURL).filter(ShortURL.short_code == short_url).first()
            if url_obj:
               url_obj.remaining_uses = usage_count
               self.db.commit()
               
            return url_obj
        except Exception as e:
            logging.error(f"Error during database insertion: {e}")
            # Rollback the transaction on error
            self.db.rollback()
            return None
        
    def add_url_access_log(self, acess_log: ShortURLAccessLog):
        try:
            self.db.add(acess_log)
            self.db.commit()
            self.db.refresh(acess_log)         
        except Exception as e:
            logging.error(f"Error during database insertion: {e}")
            # Rollback the transaction on error
            self.db.rollback()
            return None
        
    def get_urls_by_user_id(self, user_id: int):
        return self.db.query(ShortURL).filter(ShortURL.user_id == user_id).all()
    
    def get_url_details_by_id(self, url_id: int):
        return self.db.query(ShortURLAccessLog).filter(ShortURLAccessLog.short_url_id == url_id).all()