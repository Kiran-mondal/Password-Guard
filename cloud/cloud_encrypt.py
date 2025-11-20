from cryptography.hazmat.primitives.ciphers.aead import AESGCM
import base64, os

class CloudEncrypt:
    def __init__(self, key: bytes):
        self.key = key

    @staticmethod
    def generate_key():
        return AESGCM.generate_key(bit_length=256)

    def secure_pack(self, data: bytes) -> str:
        nonce = os.urandom(12)
        aes = AESGCM(self.key)
        encrypted = aes.encrypt(nonce, data, None)
        return base64.b64encode(nonce + encrypted).decode()

    def secure_unpack(self, encoded: str) -> bytes:
        raw = base64.b64decode(encoded)
        nonce, encrypted = raw[:12], raw[12:]
        aes = AESGCM(self.key)
        return aes.decrypt(nonce, encrypted, None)
      
