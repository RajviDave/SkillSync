import requests
from dotenv import load_dotenv
import os


owner=input("Enter Username")
repo=input("Input repo name")
token=os.getenv("GITHUB_TOKEN")

url=f"https://api.github.com/repos/{owner}/{repo}/languages"

headers={
    "Accept": "application/vnd.github+json",
    "Authorization": f"Bearer {token}",
    "X-GitHub-Api-Version": "2022-11-28"
}

response = requests.get(url,headers=headers)

print(response.status_code)
print(response.json())
