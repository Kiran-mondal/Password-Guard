## 2024-08-24 - [Connection Pooling for Remote API Checks]
**Learning:** The application was establishing a new TCP/SSL connection for every single password breach check against `api.pwnedpasswords.com`. Since FastAPI handles multiple concurrent users, this lack of connection pooling adds ~100-150ms of unnecessary network handshake latency per scan.
**Action:** Always use `requests.Session()` (or `httpx.AsyncClient`) for repeated API calls to the same host to leverage HTTP keep-alive and connection pooling.
