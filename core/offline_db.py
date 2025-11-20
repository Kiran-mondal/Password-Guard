import sqlite3, hashlib, os

DB_PATH = "offline_leaks/leaks_hashes.db"

def offline_check(password: str) -> bool:
    if not os.path.exists(DB_PATH):
        return False

    sha1_hash = hashlib.sha1(password.encode("utf-8")).hexdigest().upper()

    con = sqlite3.connect(DB_PATH)
    cur = con.cursor()
    result = cur.execute("SELECT hash FROM leaks WHERE hash = ?", (sha1_hash,)).fetchone()
    con.close()

    return result is not None
  
