import hashlib

# AES Encryption
AES_KEY_SIZE = 32          # 256-bit key
AES_MODE = "AES-GCM"       # authenticated encryption

# Password Hashing
HASH_ALGORITHM = hashlib.sha256
HASH_ROUNDS = 200000       # PBKDF2 rounds

# Local Vault
VAULT_FILE = "database/vault.db"
VAULT_LOCK = True
