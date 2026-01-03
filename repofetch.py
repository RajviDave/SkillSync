import requests
import os
from dotenv import load_dotenv

token=os.getenv("GITHUB_TOKEN")

url="https://api.github.com/repositories"

headers={
   "Accept": "application/vnd.github+json",
    "Authorization": f"Bearer {token}",
    "X-GitHub-Api-Version": "2022-11-28"
}

response = requests.get(url,header=headers)

print(response.status_code)