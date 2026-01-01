import requests
import nltk

response=requests.get("https://github.com/ukhirani")
print(response.status_code)
content=(response.content)

file_path = "new_file.txt"
with open(file_path, 'w') as file:
    file.write(content)

print({file_path})