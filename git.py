import dotenv
import requests
import os
import json
from dotenv import load_dotenv
import numpy as np
from numpy.linalg import norm
from sentence_transformers import SentenceTransformer
from languages import domain_to_languages
from domain import *
from domain_match import *

dotenv.load_dotenv()

GIT_TOKEN=os.getenv("GITHUB_TOKEN")

headers={
    "Accept" : "application/vnd.github+json",
    "Authorization": f"Bearer {GIT_TOKEN}",
    "X-GitHub-Api-Version": "2022-11-28",
}

def git(username, domains):
    if not username:
        return []

    print(f"DEBUG: Fetching repos for {username}...")
    
    url = f"https://api.github.com/users/{username}/repos"
    response = requests.get(url, headers=headers)

    if response.status_code != 200:
        print(f"GitHub API Error: {response.status_code} - {response.text}")
        return []

    repos = response.json()
    if not isinstance(repos, list):
        return []

    # 1. Collect all languages from all repos
    user_languages = {}
    
    # Limit to first 10 repos to avoid rate limits/timeouts if user has many repos
    for repo in repos[:10]: 
        repo_name = repo["name"]
        lang_url = f"https://api.github.com/repos/{username}/{repo_name}/languages"
        
        lang_res = requests.get(lang_url, headers=headers)
        if lang_res.status_code == 200:
            data = lang_res.json()
            for lan, size in data.items():
                user_languages[lan] = user_languages.get(lan, 0) + size

    print("DEBUG: User Languages from GitHub:", user_languages)

    # 2. Filter languages based on Domains
    final_languages = set()

    # Handle if domains is a List or a Dictionary
    domain_iterable = domains.keys() if isinstance(domains, dict) else domains

    for domain in domain_iterable:
        # Check if we have a mapping for this domain
        if domain in domain_to_languages:
            required_langs = domain_to_languages[domain]
            
            # Check if user has ANY of these languages
            for lan in required_langs:
                if lan in user_languages:
                    final_languages.add(lan)

    return list(final_languages)