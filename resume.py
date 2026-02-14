import pdfplumber
import re
import nltk
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from skills import domain_skills

def resume(pdf_path, domains):

    # --- Step 1: Extract Text from PDF ---
    all_text = " "
    with pdfplumber.open(pdf_path) as pdf:
        for page in pdf.pages:
            single_page_text = page.extract_text()
            if single_page_text:
                all_text += '\n' + single_page_text

    # --- Step 2: Clean & Tokenize Text ---
    all_text = all_text.lower()
    # Keep spaces clean to detect multi-word skills like "data science"
    clear_text = re.sub(r'[^a-zA-Z0-9\s]', ' ', all_text) 

    stop_words = set(stopwords.words('english'))
    tokens = word_tokenize(clear_text)
    
    # Use a set for O(1) lookup speed for single words
    filtered_tokens = set([word for word in tokens if word not in stop_words])

    # --- Step 3: Calculate Score ---
    scores = {}
    
    # Iterate through the domains required by the JD
    for domain_name in domains.keys():
        
        # Only proceed if we have skills defined for this domain in skills.py
        if domain_name in domain_skills:
            
            matched_count = 0
            total_possible_skills = 0
            
            # domain_skills structure is: Domain -> Category -> List of Skills
            for category, skill_list in domain_skills[domain_name].items():
                
                for skill in skill_list:
                    skill_lower = skill.lower()
                    total_possible_skills += 1 # Count every skill as a potential point
                    
                    is_matched = False
                    
                    # Logic: 
                    # If skill has spaces (e.g., "machine learning"), search raw text.
                    # If skill is one word (e.g., "python"), search the token set.
                    if " " in skill_lower:
                        if skill_lower in clear_text:
                            is_matched = True
                    else:
                        if skill_lower in filtered_tokens:
                            is_matched = True
                            
                    if is_matched:
                        matched_count += 1
            
            # --- Step 4: Generate Score ---
            if total_possible_skills > 0:
                percentage = (matched_count / total_possible_skills) * 100
                # Returns format "65/100"
                scores[domain_name] = f"{int(percentage)}/100"
            else:
                scores[domain_name] = "0/100"
        else:
            # Handle case where domain is found in JD but not in our skills DB
            scores[domain_name] = "N/A"

    return scores