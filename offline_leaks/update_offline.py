import os, requests, gzip, shutil, sqlite3

UPDATE_URL = "https://raw.githubusercontent.com/PasswordGuardCloud/data/main/hashes.txt.gz"
DB_PATH = "offline_leaks/leaks_hashes.db"

def update_db():
    print("\n☁️ Updating Offline Leak Database...")
    tmp_gz = "offline_leaks/update.gz"
    r = requests.get(UPDATE_URL, stream=True)
    with open(tmp_gz, "wb") as f:
        for chunk in r.iter_content(1024*1024):
            f.write(chunk)

    extracted = "offline_leaks/temp.txt"
    with gzip.open(tmp_gz, 'rb') as f_in:
        with open(extracted, 'wb') as f_out:
            shutil.copyfileobj(f_in, f_out)

    con = sqlite3.connect(DB_PATH)
    cur = con.cursor()
    with open(extracted, "r") as f:
        for line in f:
            h = line.split(":")[0].strip()
            if len(h) == 40:
                cur.execute("INSERT OR IGNORE INTO leaks(hash) VALUES(?)", (h,))
    con.commit()
    con.close()

    os.remove(tmp_gz)
    os.remove(extracted)
    print("🔄 Update Complete!")

if __name__ == "__main__":
    update_db()

