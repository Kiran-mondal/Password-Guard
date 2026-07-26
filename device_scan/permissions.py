import os
import platform

class PermissionManager:
    def __init__(self):
        self.os_type = platform.system()

    def ask_access(self):
        print("\n🔐 This feature needs access to saved passwords on your device.")
        
        if self.os_type == "Windows":
            return self._check_windows_admin()
        elif self.os_type == "Linux" and "ANDROID_ARGUMENT" in os.environ:
            return self._request_android_permissions()
        elif self.os_type == "Darwin": # macOS
            print("⚠️ macOS requires 'Full Disk Access' from System Preferences.")
            return True # macOS এ পপ-আপ অটোমেটিক আসে
        else:
            ans = input("Allow scanning? (yes/no): ").lower()
            return ans == "yes"

    def _check_windows_admin(self):
        """Windows-এ Chrome/Edge ডাটাবেস পড়তে Administrator পারমিশন লাগে"""
        try:
            import ctypes
            is_admin = ctypes.windll.shell32.IsUserAnAdmin()
            if not is_admin:
                print("❌ Permission Denied! Please right-click and run as 'Administrator'.")
                return False
            return True
        except:
            return False

    def _request_android_permissions(self):
        """Android-এ স্টোরেজ বা রুট পারমিশন রিকোয়েস্ট করা"""
        try:
            from android.permissions import request_permissions, Permission
            request_permissions([Permission.READ_EXTERNAL_STORAGE, Permission.WRITE_EXTERNAL_STORAGE])
            
            # Chrome এর অ্যাপ ডাটা (/data/data/com.android.chrome/...) পড়তে Android-এ Root লাগে।
            print("⚠️ Note: Reading Chrome app data on Android requires a Rooted device.")
            return True
        except ImportError:
            print("📱 Android environment not detected fully, but proceeding...")
            return True

# এক্সপোর্ট ইন্সট্যান্স
perm_manager = PermissionManager()
            
