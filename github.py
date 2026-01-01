import requests
import nltk

response=requests.get("https://github.com/ukhirani")
print(response.status_code)
content=(response.content)
words=nltk.corpus.content.words()