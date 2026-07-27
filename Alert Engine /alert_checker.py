from core.password_checker import check_password

def run_alert(password):
    report = check_password(password)

    # Avoid logging password-derived analysis details in clear text.

    # 🚨 Critical Condition (Leak + Weak)
    if report["leaked"] and not report["strong"]:
        print("🚨 CRITICAL ALERT: Device password is leaked + weak!")

    # ⚠️ Other conditional alerts
    elif report["leaked"]:
        print("⚠️ WARNING: Password found in leaked database!")

    elif not report["strong"]:
        print("⚠️ Weak Password: Improve characters and length!")

    return report
