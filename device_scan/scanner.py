from core.ai_strength import AIStrength
from core.breach_check import BreachCheck

class DeviceSmartScan:
    def __init__(self):
        self.ai = AIStrength()
        self.breach = BreachCheck()

    def analyze(self, password):
        ai = self.ai.analyze(password)
        leaked = self.breach.check(password)

        return {
            "password": password,
            "ai_score": ai["score"],
            "entropy": ai["entropy"],
            "leaked": leaked,
            "strong": ai["strong"]
        }
