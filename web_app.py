# Inside web_app.py
import asyncpg
import os

async def get_db_connection():
    """Create a fresh connection for serverless environments."""
    return await asyncpg.connect(os.getenv("NEON_DATABASE_URL"))

# Then update your /api/scan route to use this connection:
@app.post("/api/scan")
async def scan_password(req: PasswordCheckRequest):
    # ... previous logic ...
    
    # Connect and log securely
    conn = await get_db_connection()
    try:
        await conn.execute("""
            INSERT INTO scan_logs (password_hash, strength_score, is_leaked)
            VALUES ($1, $2, $3)
        """, pwd_hash, strength_data["score"], is_leaked)
    finally:
        await conn.close() # Always close the connection in serverless functions
        
    # ... return response ...
  
