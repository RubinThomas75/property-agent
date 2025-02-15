import os
import jwt
import requests
import datetime
from fastapi import APIRouter, HTTPException
from fastapi.responses import JSONResponse
from pydantic import BaseModel
from app.api.dependencies import get_db_connection  # ✅ Import shared DB function

router = APIRouter()

JWT_SECRET = os.getenv("JWT_SECRET", "your-secret-key")

class GoogleTokenRequest(BaseModel):
    token: str

def verify_google_token(token: str):
    GOOGLE_CLIENT_ID = os.getenv("GOOGLE_CLIENT_ID")
    google_url = f"https://oauth2.googleapis.com/tokeninfo?id_token={token}"

    response = requests.get(google_url)
    if response.status_code != 200:
        raise HTTPException(status_code=400, detail="Invalid Google token")

    payload = response.json()
    if payload.get("aud") != GOOGLE_CLIENT_ID:
        raise HTTPException(status_code=400, detail="Invalid audience")

    return payload

@router.post("/verify-google")
async def verify_google(data: GoogleTokenRequest):
    """ Handles Google Login Token Verification and Stores User in DB """
    google_token = data.token
    if not google_token:
        raise HTTPException(status_code=400, detail="Token is missing")

    user_info = verify_google_token(google_token)

    # Extract user info
    user_id = user_info["sub"]  # Google User ID
    email = user_info["email"]
    name = user_info.get("name", "")
    picture = user_info.get("picture", "")

    # ✅ Get database connection
    conn = get_db_connection()
    cursor = conn.cursor()

    try:
        cursor.execute("""
            INSERT INTO users (user_id, email, name, picture, last_logged_in)
            VALUES (%s, %s, %s, %s, NOW())
            ON CONFLICT (email) DO UPDATE 
            SET last_logged_in = NOW();
        """, (user_id, email, name, picture))

        conn.commit()

    except Exception as e:
        conn.rollback()
        raise HTTPException(status_code=500, detail=f"Database error: {str(e)}")

    finally:
        cursor.close()
        conn.close()

    # ✅ Generate JWT for backend authentication
    backend_token = jwt.encode(
        {
            "sub": email,
            "name": name,
            "picture": picture,
            "exp": datetime.datetime.utcnow() + datetime.timedelta(days=7),
        },
        JWT_SECRET,
        algorithm="HS256",
    )

    return JSONResponse(content={"token": backend_token})
