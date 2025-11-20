import hashlib, requests

class BreachCheck:
    def check(self, password):
        sha1 = hashlib.sha1(password.encode('utf-8')).hexdigest().upper()
        first, tail = sha1[:5], sha1[5:]
        url = f"https://api.pwnedpasswords.com/range/{first}"
        result = requests.get(url).text
        return tail in result
      
