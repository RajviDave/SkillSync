import dotenv
import requests
import os
import json
from dotenv import load_dotenv
import numpy as np
from numpy.linalg import norm
from sentence_transformers import SentenceTransformer
from languages import domain_to_languages
from domain import top_domain


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
final_dictionary={}
for repo in final_response:
    repo_name=repo["name"]
    
    headers1={
        "Accept": "application/vnd.github+json",
        "Authorization": f"Bearer {GIT_TOKEN}",
        "X-GitHub-Api-Version": "2022-11-28",
    }

    response1=requests.get(f"https://api.github.com/repos/{username}/{repo_name}/languages",headers=headers1)

    
    response=response1.json()
    
    for lan in response:
        if lan not in final_dictionary:
            final_dictionary[lan]=response[lan]
        else:
            final_dictionary[lan]=final_dictionary[lan]+response[lan]

# print(final_dictionary)
sorted_dict_desc = dict(sorted(final_dictionary.items(), key=lambda item: item[1], reverse=True))
print(sorted_dict_desc)