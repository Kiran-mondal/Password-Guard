## 2024-08-24 - [Connection Pooling for Remote API Checks]
**Learning:** The application was establishing a new TCP/SSL connection for every single password breach check against `api.pwnedpasswords.com`. Since FastAPI handles multiple concurrent users, this lack of connection pooling adds ~100-150ms of unnecessary network handshake latency per scan.
**Action:** Always use `requests.Session()` (or `httpx.AsyncClient`) for repeated API calls to the same host to leverage HTTP keep-alive and connection pooling.

## 2024-08-25 - [Decouple Non-Critical Database Writes from HTTP Request Cycle]
**Learning:** The FastAPI application was blocking the main HTTP response cycle to synchronously invoke an asynchronous Postgres write (`asyncio.run(log_scan_to_neon(...))`) within `core/breach_check.py`. This caused substantial delays (15-20s per 10 requests) and `asyncio.run` calls within an already running FastAPI event loop often fail silently.
**Action:** Use FastAPI's `BackgroundTasks` to offload non-critical telemetry or database logging operations out of the main request cycle, vastly improving latency (to ~0.9s per 10 requests) and reliability.
