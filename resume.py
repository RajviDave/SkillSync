import pdfplumber
import re

pdf_path='Rajvi_Resume (2).pdf'
print(pdf_path)

all_text=" "

with pdfplumber.open(pdf_path) as pdf:
    for page in pdf.pages:
        single_page_text=page.extract_text()
        all_text+='\n'+single_page_text

all_text=all_text.lower()
all_text=re.sub(r'[^a-zA-Z0-9\s]',all_text)

