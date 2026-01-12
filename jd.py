from google import genai
import os
from dotenv import load_dotenv

load_dotenv()


# 1. Initialize the Client with your API Key
client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))

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
user_prompt = "print 1 to 5 with its multiplier and divider "
generate_text(user_prompt)


