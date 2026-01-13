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
  
all_value=sum(languages.values())
print(all_value)

final={}

for key,value in languages.items():
    single_value=(value / all_value) * 100
    final[key]=final.get(key,0)+single_value

# print(final)

final_sorted=dict(sorted(final.items(), key=lambda item:item[1], reverse=True))

print(final_sorted)