import http.client
import json
import os
import requests

owner = input("Enter username = ")

conn = http.client.HTTPSConnection("api.github.com")

headers = {
    "Accept": "application/vnd.github+json",
    "User-Agent": "Python-App",
    "Authorization": f"Bearer {os.getenv('GITHUB_TOKEN')}"
}

conn.request("GET", f"/users/{owner}/repos", headers=headers)

res = conn.getresponse()
data = res.read()
languages={}

repos = json.loads(data.decode("utf-8"))

# extract repo names
repo_names = [repo["name"] for repo in repos]

print(repo_names)

for repo in repo_names:
    
    url=f"https://api.github.com/repos/{owner}/{repo}/languages"

    headers={
        "Accept": "application/vnd.github+json",
        "Authorization": f"Bearer {os.getenv('GITHUB_TOKEN')}",
        "X-GitHub-Api-Version": "2022-11-28"
    }
   
    response = requests.get(url,headers=headers) 
    dictionary=response.json()
    
    for key,value in dictionary.items():

        if key in languages:
            languages[key]=languages[key]+value
        else:
            languages[key]=value

print(languages)       
languages=list(languages)  
print(type(languages)) 

