# api/index.py
import sys
import os
import re 
import logging
import hashlib

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(BASE_DIR)

# বর্তমান 'api' ফোল্ডারটিকেও Path-এ যোগ করা হলো যাতে 'html_views.py' পাওয়া যায়
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from fastapi import FastAPI, Request
from pydantic import BaseModel, Field
from fastapi.responses import HTMLResponse, Response
from fastapi.staticfiles import StaticFiles

# 🛡️ Rate Limiting 
from slowapi import Limiter, _rate_limit_exceeded_handler
from slowapi.util import get_remote_address
from slowapi.errors import RateLimitExceeded

from core.ai_strength import AIStrength
from core.breach_check import breach_check

# 🧩 নতুন ফাইল থেকে HTML ডিজাইনগুলো ইম্পোর্ট করা হলো
from html_views import (
    get_base_html, get_home_content, get_about_content, 
    get_cli_content, get_github_content, get_sitemap_content
)

# 🛡️ লগিং সেটআপ
logging.basicConfig(level=logging.ERROR, format="%(asctime)s - %(levelname)s - %(message)s")
logger = logging.getLogger(__name__)

ai = AIStrength()
app = FastAPI(title="Password Guard Web")

# 🛡️ Rate Limiter সেটআপ
limiter = Limiter(key_func=get_remote_address)
app.state.limiter = limiter
app.add_exception_handler(RateLimitExceeded, _rate_limit_exceeded_handler)

app.mount("/static", StaticFiles(directory=os.path.join(BASE_DIR, "static")), name="static")

# 🛡️ Input Validation
class PasswordCheckRequest(BaseModel):
    password: str = Field(..., max_length=128, description="User password for scanning")

# ================= 🌐 WEB ROUTES =================
@app.get("/", response_class=HTMLResponse)
async def home_page():
    return HTMLResponse(get_base_html("Home", "/", get_home_content()))

@app.get("/about", response_class=HTMLResponse)
async def about_page():
    return HTMLResponse(get_base_html("About", "/about", get_about_content()))

@app.get("/cli", response_class=HTMLResponse)
async def cli_page():
    return HTMLResponse(get_base_html("CLI Setup", "/cli", get_cli_content()))

@app.get("/github", response_class=HTMLResponse)
async def github_preview_page():
    return HTMLResponse(get_base_html("Projects Preview", "/github", get_github_content()))

# ================= 🛡️ SITEMAP ROUTE =================
@app.get("/sitemap.xml", response_class=Response)
async def get_sitemap():
    return Response(content=get_sitemap_content(), media_type="application/xml")

# ================= 🛡️ API ROUTE (SECURED) =================
@app.post("/api/scan")
@limiter.limit("15/minute")
async def scan_password(request: Request, req: PasswordCheckRequest):
    pwd = req.password
    
    strength_data = ai.analyze(pwd)
    is_leaked = breach_check(pwd)
    
    has_upper = bool(re.search(r'[A-Z]', pwd))
    has_lower = bool(re.search(r'[a-z]', pwd))
    has_num = bool(re.search(r'[0-9]', pwd))
    has_special = bool(re.search(r'[^A-Za-z0-9]', pwd))
    
    if len(pwd) >= 8 and has_upper and has_lower and has_num and has_special:
        strength_data["score"] = 100
        strength_data["suggestion"] = ["Excellent! Your password meets all standard security criteria."]
    
    pwd_hash = hashlib.sha256(pwd.encode()).hexdigest()
    
    try:
        from cloud.neon_db import get_db_connection
        conn = await get_db_connection()
        if conn:
            await conn.execute("""
                INSERT INTO scan_logs (password_hash, strength_score, is_leaked)
                VALUES ($1, $2, $3)
            """, pwd_hash, strength_data["score"], is_leaked)
            await conn.close() 
    except Exception as e:
        logger.error(f"Database insertion failed: {str(e)}")
    
    return {
        "status": "success",
        "leaked": is_leaked,
        "ai_score": strength_data["score"],
        "entropy": strength_data["entropy"],
        "suggestions": strength_data["suggestion"]
    }
    
