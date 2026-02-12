from domain import *
from skills import domain_skills
import re
import nltk
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize

def match_domain(job_description):
    jd=job_description.lower()
    jd=re.sub(r'[^a-zA-Z0-9\s]', ' ', jd)
    clean_text=jd   

    stop_words = set(stopwords.words('english'))
    tokens = word_tokenize(clean_text.lower())

    filtered_tokens = [word for word in tokens if word not in stop_words]

    domains={}
    for domain,keyword_list in domain_keywords.items():
        for keyword in keyword_list:
            if " " in keyword:
                if keyword in clean_text:
                    domains[domain] = domains.get(domain, 0) + 1  
            else:
                if keyword in filtered_tokens:
                    domains[domain] = domains.get(domain, 0) + 1
                
    return domains