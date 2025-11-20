import re
import math

class AIStrength:
    def analyze(self, password: str) -> dict:
        score = 0

        length = len(password)

        # Length score
        if length >= 12:
            score += 40
        elif length >= 8:
            score += 25
        else:
            score += 10

        # Character diversity
        types = sum([
            bool(re.search(r"[A-Z]", password)),
            bool(re.search(r"[a-z]", password)),
            bool(re.search(r"[0-9]", password)),
            bool(re.search(r"[\W_]", password)),
        ])
        score += types * 10

        # Predictability reduction (AI logic)
        predictable = [
            "123", "111", "abc", "password", "qwerty"
        ]
        if any(p in password.lower() for p in predictable):
            score -= 35

        # Entropy Calculation
        pool = 0
        pool += 26 if re.search(r"[a-z]", password) else 0
        pool += 26 if re.search(r"[A-Z]", password) else 0
        pool += 10 if re.search(r"[0-9]", password) else 0
        pool += 33 if re.search(r"[\W_]", password) else 0

        entropy = 0 if pool == 0 else round(math.log2(pool ** length), 2)

        return {
            "score": max(0, min(score, 100)),
            "entropy": entropy,
            "strong": score >= 70,
            "suggestion": self.suggest(password)
        }

    def suggest(self, password):
        suggestions = []

        if len(password) < 12:
            suggestions.append("Use at least 12 characters")

        if not re.search(r"[A-Z]", password):
            suggestions.append("Add uppercase letters")

        if not re.search(r"[a-z]", password):
            suggestions.append("Add lowercase letters")

        if not re.search(r"[0-9]", password):
            suggestions.append("Include numbers")

        if not re.search(r"[\W_]", password):
            suggestions.append("Use special symbols (!@#$%)")

        return suggestions

