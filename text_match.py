from domain import *
from resume import domain_skills
import re
import nltk
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize

j_d=input("Enter job description = ")
jd=j_d.lower()
jd=re.sub(r'[^a-zA-Z0-9\s]', ' ', jd)
clean_text=jd
# print(clean_text)

stop_words = set(stopwords.words('english'))
tokens = word_tokenize(j_d.lower())

filtered_tokens = [word for word in tokens if word not in stop_words]
# print(filtered_tokens)

matched_domains={}
for domain,keyword_list in domain_keywords.items():
    for keyword in keyword_list:
        if " " in keyword:
            if keyword in clean_text:
                matched_domains[domain] = matched_domains.get(domain, 0) + 1  
        else:
            if keyword in filtered_tokens:
                matched_domains[domain] = matched_domains.get(domain, 0) + 1
            

print(matched_domains)