import re, hashlib, requests, math

def check_leak(password):
    sha1 = hashlib.sha1(password.encode("utf-8")).hexdigest().upper()
    prefix, suffix = sha1[:5], sha1[5:]
    url = f"https://api.pwnedpasswords.com/range/{prefix}"
    response = requests.get(url).text
    return suffix in response

def password_strength(password):
    score = 0

    # Length Check
    if len(password) >= 8: score += 1
    if len(password) >= 12: score += 1

    # Character Diversity
    if re.search(r"[A-Z]", password): score += 1
    if re.search(r"[a-z]", password): score += 1
    if re.search(r"\d", password): score += 1
    if re.search(r"[@$!%*?&^#]", password): score += 1

    # Entropy Calculation
    charset = 0
    if re.search(r"[a-z]", password): charset += 26
    if re.search(r"[A-Z]", password): charset += 26
    if re.search(r"\d", password): charset += 10
    if re.search(r"[@$!%*?&^#]", password): charset += 20
    entropy = round(len(password) * math.log2(charset), 2) if charset else 0

    # Strength Labels
    levels = ["Very Weak", "Weak", "Medium", "Strong", "Very Strong"]
    strength = levels[min(score, 4)]
    return strength, entropy
