## 2024-08-24 - [Exposed Sensitive Data in logs]
**Vulnerability:** Found `print(f"🚨 CRITICAL: {pwd} = LEAKED + WEAK")` in `ai/ai_assistant.py`.
**Learning:** It logged plaintext passwords directly into standard output when doing device scan.
**Prevention:** Mask passwords, log a truncated or sanitized version instead.
## 2026-08-26 - [Missing CORS Security Header in FastAPI API]
**Vulnerability:** The FastAPI application (`api/index.py`) did not have CORS protection setup, allowing external domains to perform unauthorized calls to the API.
**Learning:** Security middleware (like `CORSMiddleware`) should be established in web servers to prevent unwanted requests, and we should define strict boundaries.
**Prevention:** Avoid relying solely on custom XSS and Frame-Options headers. Implement an actual `CORSMiddleware` and restrict `allow_origins` to known safe domains.
