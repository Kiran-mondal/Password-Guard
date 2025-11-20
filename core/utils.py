import os, re

def clear():
    os.system('cls' if os.name == 'nt' else 'clear')

def validate_input(text):
    return bool(re.match(r"^[\w\- @!#%^&*()]+$", text))

def load_key(path="database/key.bin"):
    if not os.path.exists(path):
        from core.encrypt import Encryptor
        key = Encryptor.generate_key()
        with open(path, "wb") as f:
            f.write(key)
        return key
    return open(path, "rb").read()

