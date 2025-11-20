#!/usr/bin/env python3
import os, sqlite3, requests, gzip, shutil
from config.app_config import save_db_choice

API_SOURCES = {
    "A": "https://downloads.pwnedpasswords.com/passwords/pwned-passwords-sha1-ordered-by-hash-v8.txt.gz",
    "B": "https://raw.githubusercontent.com/PasswordGuardCloud/data/main/hashes.txt.gz"
}

DB_DIR = "offline_leaks"
DB_PATH = os.path.join(DB_DIR, "leaks_hashes.db")

def download_and_build(source_url):
    temp_gz = os.path.join(DB_DIR, "hash_download.gz")
    print("\n⬇️ Downloading leak hashes (this may take time)...")

    r = requests.get(source_url, stream=True)
    with open(temp_gz, "wb") as f:
        for chunk in r.iter_content(1024 * 1024):
            f.write(chunk)

    print("📦 Extracting...")
    extracted_file = os.path.join(DB_DIR, "temp_hashes.txt")
    with gzip.open(temp_gz, 'rb') as f_in:
        with open(extracted_file, 'wb') as f_out:
            shutil.copyfileobj(f_in, f_out)

    print("🗄 Building SQLite DB...")
    build_sqlite_db(extracted_file)

    os.remove(temp_gz)
    os.remove(extracted_file)
    print("🎉 Setup Completed Successfully!")

def build_sqlite_db(hash_file):
    con = sqlite3.connect(DB_PATH)
    cur = con.cursor()
    cur.execute("CREATE TABLE IF NOT EXISTS leaks(hash TEXT PRIMARY KEY)")
    cur.execute("DELETE FROM leaks")

    with open(hash_file, "r") as f:
        for line in f:
            hash_val = line.split(":")[0].strip()
            if len(hash_val) == 40:
                cur.execute("INSERT OR IGNORE INTO leaks(hash) VALUES(?)", (hash_val,))
    con.commit()
    con.close()

def main():
    print("\n🔐 PasswordGuard Offline Leak Setup")
    print("\nChoose DB size:")
    print("[1] Small (5 Million)")
    print("[2] Medium (14 Million)")
    print("[3] Large (Full 600M)")

    size = input("Choose 1/2/3: ")

    print("\nChoose Download Source:")
    print("[A] HaveIBeenPwned (Official)")
    print("[B] PasswordGuard Cloud (Faster)")
    choice = input("Choose A/B: ").upper()

    save_db_choice(size, choice)
    download_and_build(API_SOURCES[choice])

if __name__ == "__main__":
    if not os.path.exists(DB_DIR):
        os.makedirs(DB_DIR)
    main()
