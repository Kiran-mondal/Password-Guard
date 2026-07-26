import os, re, socket

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

def is_online():
    """চেক করে ডিভাইসে ইন্টারনেট কানেকশন আছে কি না।"""
    try:
        # ক্লাউডফ্লেয়ার ডিএনএস (1.1.1.1) এ ২ সেকেন্ডের জন্য পিং করে চেক করবে
        socket.create_connection(("1.1.1.1", 53), timeout=2)
        return True
    except OSError:
        pass
    return False
    
