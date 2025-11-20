import requests, hashlib
from core.offline_db import offline_check

PWNED_URL = "https://api.pwnedpasswords.com/range/"

def online_check(password):
    sha1 = hashlib.sha1(password.encode("utf-8")).hexdigest().upper()
    head, tail = sha1[:5], sha1[5:]
    response = requests.get(PWNED_URL + head).text
    return tail in response

def breach_check(password):
    offline = offline_check(password)
    online = False

    try:
        online = online_check(password)
    except:
        pass  # no internet, ignore

    return offline or online

