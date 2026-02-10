import pdfplumber
import re
import nltk
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from skills import domain_skills
from text_match import matched_domains

pdf_path='Rajvi_Resume (2).pdf' 
print(pdf_path)

all_text=" "

with pdfplumber.open(pdf_path) as pdf:
    for page in pdf.pages:
        single_page_text=page.extract_text()
        all_text+='\n'+single_page_text

all_text=all_text.lower()
clear_text=re.sub(r'[^a-zA-Z0-9\s]',' ',all_text)
print(clear_text)

stop_words = set(stopwords.words('english'))
tokens = word_tokenize(clear_text.lower())

filtered_tokens = [word for word in tokens if word not in stop_words]

filtered_tokens=set(filtered_tokens)
print(filtered_tokens)

languages={}

for key,value in matched_domains.items():
    if key in domain_skills:
        for category, skill_list in domain_skills[key].items():
            for pointer in skill_list:
                if " " in pointer:
                    if pointer in clear_text:
                        languages[key] = languages.get(key, 0) + 1
                else:
                    if pointer in filtered_tokens:
                        languages[key] = languages.get(key, 0) + 1

print(languages)
