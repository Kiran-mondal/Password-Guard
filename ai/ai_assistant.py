# ==========================================================
# AI Assistant Engine for Password Guard
# User–Driven Commands + Smart AI Suggestions
# ==========================================================

import re
from core.breach_check import run_breach_scan
from core.password_strength import password_strength_score
from core.offline_db import check_local_leak
from utils.stats import save_password_stats

class AIAssistant:
    def __init__(self):
        self.actions = {
            "check password": self.check_password,
            "scan device": self.scan_device,
            "password stats": self.show_stats,
            "recommend": self.recommend_strong_pass,
        }

    # ---------------- USER COMMAND SELECTOR ----------------
    def handle(self, user_text):
        user_text = user_text.lower().strip()

        for key, action in self.actions.items():
            if key in user_text:
                return action()

        if re.search(r"(test|check) [a-zA-Z0-9!@#$%^&*()_+=-]+", user_text):
            pwd = user_text.split()[-1]
            return self.check_custom_password(pwd)

        return "🤖 I didn’t understand. Try: 'check password' | 'scan device' | 'password stats'"

    # ================== FEATURES ==========================

    def check_password(self):
        pwd = input("🔐 Enter password to check: ")
        return self._full_check(pwd)

    def check_custom_password(self, pwd):
        return self._full_check(pwd)

    def _full_check(self, pwd):
        result = run_breach_scan(pwd)
        strength = password_strength_score(pwd)
        save_password_stats(pwd, result, strength)

        if result["leaked"] and strength < 3:
            return "🚨 CRITICAL ALERT: Password leaked + weak!"

        if result["leaked"]:
            return "⚠️ LEAKED password, change immediately!"

        if strength < 3:
            return "🔐 Not leaked, but weak. Improve!"

        return "✔️ Safe & Strong! Not leaked."

    # ------------------------------------------------------

    def scan_device(self):
        print("📱 Scanning saved device passwords...")
        leaked_count, weak_count = 0, 0

        with open("device/saved_passwords.txt", "r") as f:
            for pwd in f.read().splitlines():
                report = run_breach_scan(pwd)
                score = password_strength_score(pwd)
                save_password_stats(pwd, report, score)

                if report["leaked"]:
                    leaked_count += 1
                if score < 3:
                    weak_count += 1

                if report["leaked"] and score < 3:
                    print(f"🚨 CRITICAL: {pwd} = LEAKED + WEAK")

        return f"\nScan Completed 🔍\nLeaked: {leaked_count}\nWeak: {weak_count}"

    # ------------------------------------------------------

    def show_stats(self):
        from utils.stats import get_stats
        stats = get_stats()
        return f"📊 Stats:\nTotal Checked: {stats['total']}\nLeaked: {stats['leaked']}\nWeak: {stats['weak']}"

    # ------------------------------------------------------

    def recommend_strong_pass(self):
        import random, string
        strong = ''.join(random.choices(string.ascii_letters + string.digits + string.punctuation, k=15))
        return f"🔐 Suggested Strong Password: {strong}"

# ==========================================================
# Export Instance
# ==========================================================
AI = AIAssistant()
