import os
import asyncpg
from dotenv import load_dotenv
from core.utils import is_online

load_dotenv()
DATABASE_URL = os.getenv("NEON_DATABASE_URL")

async def get_db_connection():
    """ইন্টারনেট থাকলে এবং URL কনফিগার করা থাকলে তবেই Neon DB তে কানেক্ট করবে।"""
    if not is_online() or not DATABASE_URL:
        return None  # অফলাইন থাকলে কানেকশন বাতিল করবে
    try:
        return await asyncpg.connect(DATABASE_URL)
    except Exception as e:
        print(f"⚠️ Neon DB Connection Failed: {e}")
        return None

async def log_scan_to_neon(pwd_hash: str, score: int, leaked: bool):
    """ইন্টারনেট থাকলে স্ক্যান রিপোর্ট Neon DB তে সেভ করবে।"""
    conn = await get_db_connection()
    
    # যদি কানেকশন না পায় (অফলাইন মোড), তাহলে ক্লাউড লগিং স্কিপ করবে
    if not conn:
        return False 
    
    try:
        await conn.execute("""
            CREATE TABLE IF NOT EXISTS scan_logs (
                id SERIAL PRIMARY KEY,
                password_hash TEXT NOT NULL,
                strength_score INTEGER NOT NULL,
                is_leaked BOOLEAN NOT NULL,
                scanned_at TIMESTAMPTZ DEFAULT NOW()
            );
        """)
        
        await conn.execute("""
            INSERT INTO scan_logs (password_hash, strength_score, is_leaked)
            VALUES ($1, $2, $3)
        """, pwd_hash, score, leaked)
        return True
    finally:
        await conn.close()
      
