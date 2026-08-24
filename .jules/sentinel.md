## 2024-08-24 - [Exposed Sensitive Data in logs]
**Vulnerability:** Found `print(f"🚨 CRITICAL: {pwd} = LEAKED + WEAK")` in `ai/ai_assistant.py`.
**Learning:** It logged plaintext passwords directly into standard output when doing device scan.
**Prevention:** Mask passwords, log a truncated or sanitized version instead.
