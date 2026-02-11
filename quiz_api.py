from flask import Flask, request, jsonify
import mysql.connector
import random

app = Flask(__name__)

def get_db_connection():
    return mysql.connector.connect(
        host="localhost",
        user="root",
        password="",
        database="auth_system"
    )

@app.route("/quiz/generate", methods=["POST"])
def generate_quiz():

    data = request.get_json()
    languages = data.get("languages", [])
    total_questions = data.get("total_questions", 10)

    if not languages:
        return jsonify({"error": "No languages provided"}), 400

    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)

    easy_count = int(total_questions * 0.4)
    medium_count = int(total_questions * 0.4)
    hard_count = total_questions - easy_count - medium_count

    questions = []

    def fetch_questions(difficulty, limit):
        placeholders = ",".join(["%s"] * len(languages))
        query = f"""
            SELECT id, language, difficulty, question,
                   optionA, optionB, optionC, optionD
            FROM quiz
            WHERE difficulty = %s
              AND language IN ({placeholders})
            ORDER BY RAND()
            LIMIT %s
        """

        params = [difficulty] + languages + [limit]
        cursor.execute(query, params)
        return cursor.fetchall()
    
    questions += fetch_questions("easy", easy_count)
    questions += fetch_questions("medium", medium_count)
    questions += fetch_questions("hard", hard_count)

    random.shuffle(questions)

    cursor.close()
    conn.close()

    return jsonify(questions)

if __name__ == "__main__":
    app.run(debug=True)
