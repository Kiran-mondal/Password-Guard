import re
from config.ai_config import load_ai_mode
from core.breach_check import breach_check
from core.ai_strength import analyze_strength
from core.vault import save_password, list_saved
from core.device_scan.scanner import scan_device_passwords
from offline_leaks.update_offline import update_db

# =========================
# 🤖 AI Command Engine
# =========================

def ai_execute(command: str):
    """
    Detects user intent and executes required actions.
    """
    command = command.lower().strip()
    ai_mode = load_ai_mode()

    # ------------ INTENT MATCHING ------------
    if re.search(r"(check|test).*password", command):
        return _handle_password_check(ai_mode)

    elif re.search(r"(scan|device).*password", command):
        return _handle_device_scan(ai_mode)

    elif re.search(r"(update.*db|sync|refresh.*database)", command):
        return _handle_update(ai_mode)

    elif re.search(r"(save).*password", command):
        return _handle_save(ai_mode)

    elif re.search(r"(list|show).*password", command):
        return list_saved()

    elif re.search(r"(suggest|strong).*password", command):
        return _handle_suggestion()

    else:
        return "❓ Unknown command. Try:\n👉 check password\n👉 scan device\n👉 update db\n👉 save password\n👉 suggest password"

# =========================
# 🔐 HANDLERS
# =========================

def _handle_password_check(ai_mode):
    pwd = input("🔑 Enter a password to check: ")

    leaked = breach_check(pwd)
    strength = analyze_strength(pwd)

    # CRITICAL ALERT 🔥
    if leaked and not strength["strong"]:
        print("🚨 CRITICAL ALERT: Password is leaked + weak!")

        if ai_mode == 3:  # Full Auto
            print("🛠 Fixing automatically...")
            return _handle_suggestion(auto=True)
        return "⚠️ Change this password immediately!"

    elif leaked:
        return "⚠️ Password is leaked, but strong. Change recommended."

    elif not strength["strong"]:
        return "🔐 Password is weak. Improve it."

    else:
        return "✅ Password safe & strong!"

def _handle_device_scan(ai_mode):
    print("📱 Scanning saved device passwords...")
    results = scan_device_passwords()

    if not results:
        return "ℹ️ No passwords detected."

    print(f"🔎 Found {len(results)} passwords.")
    action = "🔐 Some are weak or leaked!"

    if ai_mode == 3:
        print("🤖 Auto-fixing passwords...")
        return _handle_suggestion(auto=True)

    return action

def _handle_update(ai_mode):
    if ai_mode == 1:
        confirm = input("☁️ Update leak database? (y/n): ").lower()
        if confirm != "y":
            return "❌ Cancelled."

    update_db()
    return "🔄 Offline DB Updated!"

def _handle_save(ai_mode):
    pwd = input("🔑 Enter password to save securely: ")

    if not analyze_strength(pwd)["strong"]:
        if ai_mode < 3:
            confirm = input("⚠️ Weak password. Save anyway? (y/n): ").lower()
            if confirm != "y":
                return "❌ Cancelled."
        else:
            print("🤖 Auto-blocking weak password. Suggesting new one...")
            return _handle_suggestion(auto=True)

    save_password(pwd)
    return "💾 Saved Successfully!"

def _handle_suggestion(auto=False):
    from core.ai_strength import suggest_password
    new_pwd = suggest_password()

    if auto:
        save_password(new_pwd)
        return f"🤖 Auto-replaced with secure password: {new_pwd}"

    return f"💡 Suggested strong password: {new_pwd}"
