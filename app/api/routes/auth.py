import os
import jwt
import requests
import datetime
from fastapi import APIRouter, HTTPException, Request
from fastapi.responses import JSONResponse
from pydantic import BaseModel

# ✅ Define router
router = APIRouter()

print("✅ auth.py is being loaded!", flush=True)

JWT_SECRET = os.getenv("JWT_SECRET", "your-secret-key")

# ✅ Define request model
class GoogleTokenRequest(BaseModel):
    token: str

def verify_google_token(token: str):
    """ Verifies the Google ID Token and extracts user info """
    GOOGLE_CLIENT_ID = os.getenv("GOOGLE_CLIENT_ID")
    google_url = f"https://oauth2.googleapis.com/tokeninfo?id_token={token}"

    print(f"🔍 Verifying token with Google: {google_url}", flush=True)

    response = requests.get(google_url)
    print(f"📡 Google API Response Code: {response.status_code}", flush=True)
    print(f"📡 Google API Response: {response.text}", flush=True)

    if response.status_code != 200:
        raise HTTPException(status_code=400, detail="Invalid Google token")

    payload = response.json()
    if payload.get("aud") != GOOGLE_CLIENT_ID:
        print(f"❌ Invalid Audience: Expected {GOOGLE_CLIENT_ID}, Got {payload.get('aud')}", flush=True)
        raise HTTPException(status_code=400, detail="Invalid audience")

    print("✅ Google Token Verified Successfully!", flush=True)
    return payload  # ✅ Returns user's Google profile data


# ✅ Correctly defined endpoint with POST method
@router.post("/verify-google")
async def verify_google(data: GoogleTokenRequest):
    """ Handles Google Login Token Verification """
    google_token = data.token
    if not google_token:
        raise HTTPException(status_code=400, detail="Token is missing")

    user_info = verify_google_token(google_token)

    # Generate JWT for backend authentication
    backend_token = jwt.encode(
        {
            "sub": user_info["email"],
            "name": user_info["name"],
            "picture": user_info["picture"],
            "exp": datetime.datetime.utcnow() + datetime.timedelta(days=7),
        },
        JWT_SECRET,
        algorithm="HS256",
    )

    print("✅ Login successful", flush=True)
    return JSONResponse(content={"token": backend_token})
