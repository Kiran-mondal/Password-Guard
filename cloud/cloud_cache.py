
class CloudCache:
    def __init__(self, db="database/cache.db"):
        self.conn = sqlite3.connect(db)
        self.create()

    def create(self):
        self.conn.execute("""
            CREATE TABLE IF NOT EXISTS cloud_cache (
                id TEXT PRIMARY KEY,
                raw_url TEXT,
                filename TEXT
            );
        """)

    def save(self, gist_id, raw_url, filename):
        self.conn.execute("INSERT OR REPLACE INTO cloud_cache (id, raw_url, filename) VALUES (?,?,?)",
                          (gist_id, raw_url, filename))
        self.conn.commit()

    def get(self):
        row = self.conn.execute("SELECT id, raw_url, filename FROM cloud_cache LIMIT 1").fetchone()
        return row if row else None
      
