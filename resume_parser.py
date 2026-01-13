import pdfplumber
import re
import sys

sys.stdout.reconfigure(encoding='utf-8')

text=""

with pdfplumber.open("Rajvi_Resume (2).pdf") as pdf:
    for page in pdf.pages:
        text+=page.extract_text() or ""

print(text)