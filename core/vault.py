VALUES (?,?,?,?)",
            (service, username, nonce, enc)
        )
        self.conn.commit()

    def get_all(self):
        rows = self.conn.execute("SELECT service, username, nonce, password FROM passwords").fetchall()
        decrypted = []
        for service, user, nonce, data in rows:
            dec = self.encryptor.decrypt(nonce, data).decode()
            decrypted.append((service, user, dec))
        return decrypted
      
