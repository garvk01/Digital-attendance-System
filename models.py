from pydantic import BaseModel
from datetime import datetime

class User(BaseModel):
    user_id: int
    name: str

class Attendance(BaseModel):
    user_id: int
    name: str
    timestamp: datetime
