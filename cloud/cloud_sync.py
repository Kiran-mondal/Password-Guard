from cloud.cloud_encrypt import CloudEncrypt
from cloud.github_api import GitHubAPI
from cloud.cloud_cache import CloudCache
from core.vault import Vault
from core.utils import load_key

class CloudSync:
    def __init__(self, token):
        self.token = token
        self.cache = CloudCache()
        key = load_key()
        self.secure = CloudEncrypt(key)
        self.github = GitHubAPI(token)

    def upload(self):
        vault = Vault().get_all()
        data = "\n".join([f"{s},{u},{p}" for s, u, p in vault])
        encrypted = self.secure.secure_pack(data.encode())

        cached = self.cache.get()
        if cached:
            res = self.github.update(cached[0], cached[2], encrypted)
        else:
            res = self.github.upload("vault.secure", encrypted)

        gist_id = res["id"]
        raw_url = list(res["files"].values())[0]["raw_url"]
        self.cache.save(gist_id, raw_url, "vault.secure")

        return True

    def download(self):
        cached = self.cache.get()
        if not cached:
            return False

        raw = self.github.download(cached[1])
        decrypted = self.secure.secure_unpack(raw).decode()
        return decrypted.split("\n")

