class PermissionManager:
    def ask_access(self):
        print("\n🔐 This feature needs access to saved passwords on your device.")
        ans = input("Allow scanning? (yes/no): ").lower()
        return ans == "yes"

