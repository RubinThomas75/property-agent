from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.api.routes import auth
from dotenv import load_dotenv
import os

app = FastAPI()
load_dotenv()

GOOGLE_CLIENT_ID = os.getenv("GOOGLE_CLIENT_ID")

# Allow frontend to communicate with backend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],  # Adjust this if your Next.js app runs elsewhere
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/api/health")
async def health_check():
    return {"status": "ok", "message": "API is running!"}

# Include API routes
app.include_router(auth.router, prefix="/api/auth")
# app.include_router(files.router, prefix="/api/files")
# app.include_router(rag.router, prefix="/api/rag")
