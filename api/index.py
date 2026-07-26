import sys
import os

# Vercel যেন মূল ডিরেক্টরির ফাইলগুলো (core, cloud) খুঁজে পায় তার জন্য এই ৩ লাইন:
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import hashlib
from fastapi import FastAPI
from pydantic import BaseModel
from contextlib import asynccontextmanager

from cloud.neon_db import create_pool, init_db, log_scan
from core.ai_strength import AIStrength
from core.breach_check import breach_check

# Initialize core components
ai = AIStrength()
db_pool = None

@asynccontextmanager
async def lifespan(app: FastAPI):
    global db_pool
    from cloud.neon_db import get_db_connection
    yield
    if db_pool:
        await db_pool.close()

# Vercel ঠিক এই 'app' ভেরিয়েবলটিই খুঁজছিল!
app = FastAPI(title="Password Guard Web API", lifespan=lifespan)

class PasswordCheckRequest(BaseModel):
    password: str

@app.post("/api/scan")
async def scan_password(req: PasswordCheckRequest):
    pwd = req.password
    
    strength_data = ai.analyze(pwd)
    is_leaked = breach_check(pwd)
    
    pwd_hash = hashlib.sha256(pwd.encode()).hexdigest()
    
    # Serverless-এর জন্য সরাসরি কানেকশন
    from cloud.neon_db import get_db_connection
    conn = await get_db_connection()
    if conn:
        try:
            await conn.execute("""
                INSERT INTO scan_logs (password_hash, strength_score, is_leaked)
                VALUES ($1, $2, $3)
            """, pwd_hash, strength_data["score"], is_leaked)
        finally:
            await conn.close() 
    
    return {
        "status": "success",
        "leaked": is_leaked,
        "ai_score": strength_data["score"],
        "entropy": strength_data["entropy"],
        "suggestions": strength_data["suggestion"]
  }
  
