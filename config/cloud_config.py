CLOUD_ENABLED = True

CLOUD_PROVIDER = "PasswordGuardCloud"   # later upgrade to firebase, supabase, etc.

CLOUD_API_ENDPOINT = "https://api.passwordguard.cloud/v1/"
CLOUD_AUTH_TOKEN = None  # runtime assignment

SYNC_INTERVAL = 1800  # auto-sync every 30 min
LOCAL_CACHE = "database/cache.db"

