from pydantic import BaseModel
from datetime import datetime

class UserCreate(BaseModel):
    user_id: str
    email: str
    name: str | None = None
    picture: str | None = None

class UserResponse(BaseModel):
    user_id: str
    email: str
    name: str | None
    picture: str | None
    last_logged_in: datetime
