import requests, hashlib
import asyncio
from core.offline_db import offline_check
from core.utils import is_online

PWNED_URL = "https://api.pwnedpasswords.com/range/"

# Reusing a session allows for HTTP keep-alive and connection pooling,
# significantly speeding up repeated network calls.
session = requests.Session()

def online_check(password):
    sha1 = hashlib.sha1(password.encode("utf-8")).hexdigest().upper()
    head, tail = sha1[:5], sha1[5:]
    response = session.get(PWNED_URL + head, timeout=3).text
    return tail in response

def breach_check(password, strength_score=0):
    """
    স্মার্ট হাইব্রিড চেক: 
    ১. ইন্টারনেট থাকলে -> ক্লাউড API দিয়ে চেক করবে এবং Neon DB তে লগ রাখবে।
    ২. ইন্টারনেট না থাকলে -> ডিভাইসের লোকাল SQLite (offline_db) ব্যবহার করবে।
    """
    is_leaked = False
    
    if is_online():
        print("🌐 Online Mode: Scanning via Cloud...")
        try:
            is_leaked = online_check(password)
            
            # Telemetry logging moved to FastAPI BackgroundTasks
                
        except requests.RequestException:
            print("⚠️ Cloud API Error: Falling back to Local Database...")
            is_leaked = offline_check(password) # API ফেইল করলে লোকাল স্ক্যানে চলে যাবে
    else:
        print("🔒 Offline Mode: Scanning via Local Device Database...")
        # ইন্টারনেট না থাকলে সম্পূর্ণভাবে লোকাল ডেটাবেজ ব্যবহার করবে (Neon বা API এক্সেস করবে না)
        is_leaked = offline_check(password)

    return is_leaked
                
