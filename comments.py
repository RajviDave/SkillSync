from textblob import TextBlob

class FeedbackComponent:
    def __init__(self):
        self.MAX_SCORE = 30  # 30% weightage

    def get_score(self, comments: list):
        """
        Takes a list of comments, analyzes sentiment, 
        and returns a score out of 30.
        """
        if not comments:
            return 0.0
        
        total_polarity = 0
        
        # Analyze sentiment for each comment
        for comment in comments:
            blob = TextBlob(comment)
            # Polarity ranges from -1 (Negative) to +1 (Positive)
            total_polarity += blob.sentiment.polarity
        
        # Calculate Average Polarity
        avg_polarity = total_polarity / len(comments)
        
        # Normalize Score:
        # We convert the range [-1, 1] into [0, 30]
        # Formula: ((Score + 1) / 2) * Max_Score
        weighted_score = ((avg_polarity + 1) / 2) * self.MAX_SCORE
        
        return round(weighted_score, 2)

# ==========================================
# MAIN EXECUTION
# ==========================================
if __name__ == "__main__":
    print("\n--- MENTOR FEEDBACK ANALYZER (30%) ---")
    
    # 1. Take Single String Input from User
    user_input = input(">>> Enter Mentor's Comment: ").strip()
    
    # 2. Convert string to list (System requires a list format)
    if user_input:
        comments_list = [user_input]
    else:
        comments_list = []

    # 3. Process the Comment
    engine = FeedbackComponent()
    final_score = engine.get_score(comments_list)
    
    # 4. Show Result
    print("-" * 30)
    print(f"📝 Input: \"{user_input}\"")
    print(f"🏆 CALCULATED SCORE: {final_score} / 30")
    print("-" * 30)