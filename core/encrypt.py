from cryptography.hazmat.primitives.ciphers.aead import AESGCM
import os

class Encryptor:
    def __init__(self, key: bytes):
        self.key = key

    @staticmethod
    def generate_key():
        return AESGCM.generate_key(bit_length=256)

    def encrypt(self, data: bytes) -> tuple:
        aes = AESGCM(self.key)
        nonce = os.urandom(12)
        encrypted = aes.encrypt(nonce, data, None)
        return nonce, encrypted

    def decrypt(self, nonce: bytes, encrypted_data: bytes) -> bytes:
        aes = AESGCM(self.key)
        return aes.decrypt(nonce, encrypted_data, None)
      
