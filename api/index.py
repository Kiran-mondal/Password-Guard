import sys
import os
import re 
import logging
import hashlib
import hmac

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(BASE_DIR)

from fastapi import FastAPI, Request, BackgroundTasks
from pydantic import BaseModel, Field
from fastapi.responses import HTMLResponse, Response
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware

# 🛡️ Rate Limiting 
from slowapi import Limiter, _rate_limit_exceeded_handler
from slowapi.util import get_remote_address
from slowapi.errors import RateLimitExceeded

from core.ai_strength import AIStrength
from core.breach_check import breach_check

# 🛡️ Error Logging
logging.basicConfig(level=logging.ERROR, format="%(asctime)s - %(levelname)s - %(message)s")
logger = logging.getLogger(__name__)

ai = AIStrength()

# 🛡️ Disable public Swagger/OpenAPI docs in production
app = FastAPI(
    title="Password Guard Web",
    docs_url=None,
    redoc_url=None,
    openapi_url=None
)

# 🛡️ Rate Limiter Setup (MUST be defined before routes)
limiter = Limiter(key_func=get_remote_address)
app.state.limiter = limiter
app.add_exception_handler(RateLimitExceeded, _rate_limit_exceeded_handler)

# 🛡️ CORS Middleware Setup (NovalNetwork Hub Added)
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost",
        "http://localhost:8000",
        "http://127.0.0.1:8000",
        "https://passwordguard.quarry.dpdns.org",
        "https://noval-network.vercel.app"
    ],
    allow_credentials=True,
    allow_methods=["GET", "POST", "OPTIONS"],
    allow_headers=["*"],
)

# 🛡️ Security Headers Middleware (Allows NovalNetwork Hub & Telegram WebApp framing)
@app.middleware("http")
async def add_security_headers(request: Request, call_next):
    response = await call_next(request)
    
    if "X-Frame-Options" in response.headers:
        del response.headers["X-Frame-Options"]
    
    response.headers["Content-Security-Policy"] = (
        "default-src 'self' https:; "
        "style-src 'self' 'unsafe-inline' https:; "
        "script-src 'self' 'unsafe-inline' https://telegram.org; "
        "img-src 'self' data: https:; "
        "frame-ancestors 'self' https://noval-network.vercel.app https://*.vercel.app https://*.dpdns.org https://*.telegram.org;"
    )
    
    response.headers["X-RateLimit-Limit"] = "15"
    response.headers["X-RateLimit-Remaining"] = "14"
    response.headers["X-RateLimit-Reset"] = "60"
    
    return response

app.mount("/static", StaticFiles(directory=os.path.join(BASE_DIR, "static")), name="static")

# 🛡️ Input Validation
class PasswordCheckRequest(BaseModel):
    password: str = Field(..., max_length=128, description="User password for scanning")

# ================= 🌐 WEB ROUTES =================

@app.get("/", response_class=HTMLResponse)
@app.get("/api/index.py", response_class=HTMLResponse, include_in_schema=False)
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
async def scan_password(request: Request, req: PasswordCheckRequest, background_tasks: BackgroundTasks):
    pwd = req.password
    
    strength_data = ai.analyze(pwd)
    import asyncio
    is_leaked = await asyncio.to_thread(breach_check, pwd)
    
    has_upper = bool(re.search(r'[A-Z]', pwd))
    has_lower = bool(re.search(r'[a-z]', pwd))
    has_num = bool(re.search(r'[0-9]', pwd))
    has_special = bool(re.search(r'[^A-Za-z0-9]', pwd))
    
    if len(pwd) >= 8 and has_upper and has_lower and has_num and has_special:
        strength_data["score"] = 100
        strength_data["suggestion"] = ["Excellent! Your password meets all standard security criteria."]
    
    # 🛡️ Keyed HMAC-SHA256 instead of raw SHA-256 to protect scan logs
    secret_pepper = os.getenv("HASH_SECRET_PEPPER", "password-guard-default-pepper-change-in-env")
    pwd_hash = hmac.new(secret_pepper.encode(), pwd.encode(), hashlib.sha256).hexdigest()
    
    try:
        from cloud.neon_db import log_scan_to_neon
        background_tasks.add_task(log_scan_to_neon, pwd_hash, strength_data["score"], is_leaked)
    except ImportError:
        logger.warning("Cloud DB telemetry setup skipped: asyncpg not installed.")
    except Exception:
        # 🛡️ Redacted error log so database credentials/URLs are never printed
        logger.error("Cloud DB telemetry setup failed: [REDACTED]")
    
    return {
        "status": "success",
        "leaked": is_leaked,
        "ai_score": strength_data["score"],
        "entropy": strength_data["entropy"],
        "suggestions": strength_data["suggestion"]
        }
