from google import genai
import os
from dotenv import load_dotenv
import json
from repofetch import final_sorted

load_dotenv()

# 1. Initialize the Client with your API Key
client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))

job_description=input("Write your job description =")
lan=str(final_sorted)

def generate_text(prompt_text):
    try:
        # 2. Call the generate_content method
        # 'gemini-2.0-flash' is recommended for its speed and free tier availability
        response = client.models.generate_content(
            model="models/gemini-2.5-flash", 
            contents=prompt_text
        )
        
        # 3. Print the result
        print("Gemini Response:")
        print("-" * 20)
        print(response.text)
        
    except Exception as e:
        print(f"An error occurred: {e}")

# Example Usage
user_prompt = f"""
    ### CONTEXT ###
    You are a Senior Technical Interviewer. 
    A candidate is applying for the Job Description (JD) below. 
    You also have their verified GitHub Language skills.

    ### INPUT DATA ###
    **Job Description:** "{job_description}"

    **Candidate's Verified Skills (from GitHub):** {lan}

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
        "options": ["A", "B", "C", "D"],
        "correct_option": "A",
        "category": "Theory" or "Coding",
        "reason": "Why you asked this (e.g., JD mentions GenAI)"
      }}
    ]

    Do not write any conversational text. Start the response with '[' and end with ']'
    """
generate_text(user_prompt)


