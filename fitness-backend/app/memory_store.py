import uuid
from datetime import date

USERS = {}        
USER_PROFILES = {}   
WEEKLY_PLANS = {}    

def new_uuid() -> str:
    return str(uuid.uuid4())

def week_start(d: date) -> date:
    return date.fromordinal(d.toordinal() - d.weekday()) 
