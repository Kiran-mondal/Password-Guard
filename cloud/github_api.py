import requests, json

class GitHubAPI:
    def __init__(self, token: str):
        self.token = token
        self.headers = {
            "Authorization": f"token {self.token}",
            "Accept": "application/vnd.github.v3+json"
        }

    def upload(self, filename, content):
        data = {
            "description": "PasswordGuard Secure Vault",
            "public": False,
            "files": {filename: {"content": content}}
        }
        response = requests.post("https://api.github.com/gists", headers=self.headers, data=json.dumps(data))
        return response.json()

    def update(self, gist_id, filename, content):
        data = {"files": {filename: {"content": content}}}
        url = f"https://api.github.com/gists/{gist_id}"
        response = requests.patch(url, headers=self.headers, data=json.dumps(data))
        return response.json()

    def download(self, raw_url):
        return requests.get(raw_url, headers=self.headers).text
      
