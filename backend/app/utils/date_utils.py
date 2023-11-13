from datetime import datetime
import pytz

timezone = 'Asia/Kolkata'
def get_created_at(timezone=timezone):
    # Get the current time in UTC
    current_utc_time = datetime.now(pytz.timezone(timezone))

    # Return the current time with UTC timezone information
    return current_utc_time.replace(tzinfo=pytz.utc)
   

def get_datetime_now(timezone='UTC'):
    tz = pytz.timezone(timezone)
    utc_now = datetime.utcnow().replace(tzinfo=pytz.utc)
    t = utc_now.astimezone(tz)
    return t