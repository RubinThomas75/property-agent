from sqlalchemy import Column, String, DateTime
from datetime import datetime
from app.core.database import Base

class User(Base):
    __tablename__ = "users"

    user_id = Column(String, primary_key=True)  # Google `sub` as a stable unique ID
    email = Column(String, unique=True, nullable=False)
    name = Column(String, nullable=True)
    picture = Column(String, nullable=True)
    last_logged_in = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
