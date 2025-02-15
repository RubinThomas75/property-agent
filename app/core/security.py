import jwt
import os
from datetime import datetime, timedelta

JWT_SECRET = os.getenv("JWT_SECRET", "your-secret-key")

def create_jwt(payload: dict):
    return jwt.encode(payload, JWT_SECRET, algorithm="HS256")
