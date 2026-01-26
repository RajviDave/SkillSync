import dotenv
import requests
import os
from dotenv import load_dotenv

dotenv.load_dotenv()

GIT_TOKEN=os.getenv("GITHUB_TOKEN")
username=input("Enter username=")

headers={
    "Accept" : "application/vnd.github+json",
    "Authorization": f"Bearer {GIT_TOKEN}",
    "X-GitHub-Api-Version": "2022-11-28",
}

response=requests.get(f"https://api.github.com/users/{username}/repos",headers=headers)

final_response=response.json()

for repo in final_response:
    repo_name=repo["name"]
    
    headers1={
        "Accept": "application/vnd.github+json",
        "Authorization": f"Bearer {GIT_TOKEN}",
        "X-GitHub-Api-Version": "2022-11-28",
    }

    response1=requests.get(f"https://api.github.com/repos/{username}/{repo_name}/languages",headers=headers1)

    print(response1.json())