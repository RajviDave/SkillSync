import http.client
import json
import os

username = input("Enter username")

conn = http.client.HTTPSConnection("api.github.com")

headers = {
    "Accept": "application/vnd.github+json",
    "User-Agent": "Python-App",
    "Authorization": f"Bearer {os.getenv('GITHUB_TOKEN')}"
}

conn.request("GET", f"/users/{username}/repos", headers=headers)

res = conn.getresponse()
data = res.read()

repos = json.loads(data.decode("utf-8"))

# extract repo names
repo_names = [repo["name"] for repo in repos]

print(repo_names)