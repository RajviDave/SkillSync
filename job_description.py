import nltk
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize

nltk.download('punkt')
nltk.download('stopwords')

text=input("Enter JD")

stop_words=set(stopwords.words('english'))

word_tokens=word_tokenize(text)
filtered_text= [word for word in word_tokens if word.lower() not in stop_words]

print(filtered_text)