import nltk
from nltk.sentiment import SentimentIntensityAnalyzer

def comments(comment_text):
    # 1. Handle empty comments (Neutral Score)
    if not comment_text or comment_text.strip() == "":
        return 50 

    # 2. Download VADER lexicon (only happens once)
    try:
        nltk.data.find('sentiment/vader_lexicon.zip')
    except LookupError:
        nltk.download('vader_lexicon')

    # 3. Analyze Sentiment
    sia = SentimentIntensityAnalyzer()
    sentiment = sia.polarity_scores(comment_text)
    
    # sentiment['compound'] ranges from -1.0 (Very Bad) to +1.0 (Very Good)
    compound_score = sentiment['compound']

    # 4. Convert -1 to 1 scale ---> 0 to 100 scale
    # Formula: ((Score + 1) / 2) * 100
    # Example: 
    #   If score is 0 (Neutral) -> (1/2)*100 = 50
    #   If score is -0.5 (Bad)  -> (0.5/2)*100 = 25
    #   If score is 0.8 (Great) -> (1.8/2)*100 = 90
    
    final_score = int(((compound_score + 1) / 2) * 100)

    return final_score