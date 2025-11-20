ALERT_ENABLED = True

# If reused more than 2 times → alert
MAX_REUSE_LIMIT = 2

# If leaked + weak → critical alert
CRITICAL_FLAGS = {
    "LEAKED": True,
    "WEAK": True
}

# Push Notification / SMS / Email (Next Update)
NOTIFICATION_CHANNELS = {
    "push": True,
    "email": False,
    "sms": False
}
