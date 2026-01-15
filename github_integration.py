"""
GitHub Integration Module
Fetches repository data from GitHub username and generates quiz questions
"""
import http.client
import json
import os
import requests
from google import genai
from dotenv import load_dotenv

load_dotenv()

def fetch_user_repos(username: str) -> list:
    """
    Fetch all repository names for a given GitHub username
    Returns list of repository names
    """
    try:
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
        
        # Extract repo names
        repo_names = [repo["name"] for repo in repos]
        return repo_names
    except Exception as e:
        print(f"Error fetching repos: {e}")
        return []

def fetch_language_stats(username: str) -> dict:
    """
    Fetch language statistics across all repositories for a user
    Returns dictionary with language percentages
    """
    repo_names = fetch_user_repos(username)
    if not repo_names:
        return {}
    
    languages = {}
    
    for repo in repo_names:
        try:
            url = f"https://api.github.com/repos/{username}/{repo}/languages"
            headers = {
                "Accept": "application/vnd.github+json",
                "Authorization": f"Bearer {os.getenv('GITHUB_TOKEN')}",
                "X-GitHub-Api-Version": "2022-11-28"
            }
            
            response = requests.get(url, headers=headers)
            if response.status_code == 200:
                dictionary = response.json()
                
                for key, value in dictionary.items():
                    if key in languages:
                        languages[key] = languages[key] + value
                    else:
                        languages[key] = value
        except Exception as e:
            print(f"Error fetching languages for {repo}: {e}")
            continue
    
    if not languages:
        return {}
    
    # Calculate percentages
    all_value = sum(languages.values())
    final = {}
    
    for key, value in languages.items():
        single_value = (value / all_value) * 100
        final[key] = single_value
    
    # Sort by percentage (descending)
    final_sorted = dict(sorted(final.items(), key=lambda item: item[1], reverse=True))
    
    return final_sorted

def generate_quiz_from_github(job_description: str, github_username: str) -> dict:
    """
    Generate quiz questions based on job description and GitHub repository data
    Returns dictionary with quiz questions or error message
    """
    try:
        # Fetch language statistics
        language_stats = fetch_language_stats(github_username)
        
        if not language_stats:
            return {
                "error": "No repository data found for this GitHub username",
                "quiz": None
            }
        
        # Initialize Gemini client
        client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))
        
        # Prepare prompt
        lan_str = str(language_stats)
        user_prompt = f"""
    ### CONTEXT ###
    You are a Senior Technical Interviewer. 
    A candidate is applying for the Job Description (JD) below. 
    You also have their verified GitHub Language skills.

    ### INPUT DATA ###
    **Job Description:** "{job_description}"

    **Candidate's Verified Skills (from GitHub):** {lan_str}

    ### YOUR TASK ###
    Generate a 5-question technical quiz (Multiple Choice) following these rules:

    1. **Analyze the JD:** Identify specific domains (e.g., "GenAI", "Computer Vision", "Cloud"). Ask 2 conceptual questions on these topics.
    2. **Language Intersection:** - If the JD implies a language (e.g., "Scripting" -> Python) AND the Candidate knows it: Ask a HARD coding snippet question.
       - If the JD requires a language the Candidate DOES NOT know: Ask a BASIC conceptual question (to test ability to learn).
    3. **Output Format:** Return ONLY raw JSON. No markdown. No text.

    ### REQUIRED JSON STRUCTURE ###
    [
      {{
        "question": "Question text...",
        "options": ["Option A", "Option B", "Option C", "Option D"],
        "correct_option": "A",
        "category": "Theory" or "Coding",
        "reason": "Why you asked this (e.g., JD mentions GenAI)"
      }}
    ]

    Do not write any conversational text. Start the response with '[' and end with ']'
    """
        
        # Generate quiz
        response = client.models.generate_content(
            model="models/gemini-2.5-flash",
            contents=user_prompt
        )
        
        # Parse JSON from response
        response_text = response.text.strip()
        
        # Try to extract JSON if wrapped in markdown
        if response_text.startswith("```json"):
            response_text = response_text[7:]
        if response_text.startswith("```"):
            response_text = response_text[3:]
        if response_text.endswith("```"):
            response_text = response_text[:-3]
        response_text = response_text.strip()
        
        quiz_data = json.loads(response_text)
        
        return {
            "error": None,
            "quiz": quiz_data,
            "language_stats": language_stats
        }
        
    except json.JSONDecodeError as e:
        return {
            "error": f"Failed to parse quiz JSON: {str(e)}",
            "quiz": None
        }
    except Exception as e:
        return {
            "error": f"Error generating quiz: {str(e)}",
            "quiz": None
        }

def calculate_github_score(github_username: str, job_description: str) -> float:
    """
    Calculate GitHub-based score (0-50) based on repository analysis
    This is a simplified scoring - can be enhanced based on:
    - Number of repositories
    - Language match with JD
    - Repository activity
    - Code quality metrics
    """
    if not github_username:
        return 0.0
    
    try:
        language_stats = fetch_language_stats(github_username)
        
        if not language_stats:
            return 0.0
        
        # Extract skills from JD (simplified - can use resumecheck logic)
        jd_lower = job_description.lower()
        matched_languages = 0
        total_languages = len(language_stats)
        
        # Check if JD mentions any of the languages the user knows
        for lang in language_stats.keys():
            if lang.lower() in jd_lower:
                matched_languages += 1
        
        # Score based on:
        # - Having repositories (base score)
        # - Language match with JD
        base_score = min(20, total_languages * 2)  # Up to 20 points for having repos
        match_score = (matched_languages / max(1, total_languages)) * 30  # Up to 30 points for matches
        
        total_score = min(50, base_score + match_score)
        return round(total_score, 2)
        
    except Exception as e:
        print(f"Error calculating GitHub score: {e}")
        return 0.0
