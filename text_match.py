from domain import *
from resume import domain_skills
import re

jd=input("Enter job description = ")
jd=jd.lower()
jd=re.sub(r'[^a-zA-Z0-9\s]', ' ', jd)
print(jd)
