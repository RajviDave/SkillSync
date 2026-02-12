from flask import Flask, request, jsonify, render_template
import os
from werkzeug.utils import secure_filename
from resume import resume
from comments import comments
from git import git
from domain_match import match_domain
import mysql.connector
import random

app = Flask(__name__)

@app.route("/")
def home():
    return render_template("input_form.html")

@app.route("/submit", methods=["POST"])
def submit_form():

    job_description = request.form.get("jd")
    resume_file = request.files.get("resume")
    mentor_comments=request.form.get("comments")
    github_username = request.form.get("git")

    UPLOAD_FOLDER = "uploads"
    os.makedirs(UPLOAD_FOLDER, exist_ok=True)

    if not job_description or not resume_file or not mentor_comments or not github_username:
        return "Missing input", 400

    if resume_file.mimetype != "application/pdf":
        return "Only PDF files are allowed", 400
    
    filename = secure_filename(resume_file.filename)
    resume_path = os.path.join(UPLOAD_FOLDER, filename)
    resume_file.save(resume_path)

    domains=match_domain(job_description)
    jd_results=match_domain(job_description)
    resume_results=resume(resume_path,domains)
    comments_results=comments(mentor_comments)
    github_results=git(github_username,domains)
    
    # TEMP: just to prove data is coming
    return jsonify({
    "resume": resume_results,
    "comments": comments_results,
    "github": github_results
    })

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
    total = int(data.get("total_questions", 15))

    if not languages:
        return jsonify({"error": "languages required"}), 400

    easy_n = int(total * 0.4)
    medium_n = int(total * 0.4)
    hard_n = total - easy_n - medium_n

    conn = get_db_connection()
    cur = conn.cursor(dictionary=True)

    def fetch(diff, limit):
        placeholders = ",".join(["%s"] * len(languages))

        query = f"""
            SELECT id, language, difficulty,
                   quistion, optionA, optionB, optionC, optionD
            FROM quiz
            WHERE difficulty = %s
            AND language IN ({placeholders})
            ORDER BY RAND()
            LIMIT %s
        """

        params = [diff] + languages + [limit]
        cur.execute(query, params)
        return cur.fetchall()

    questions = []
    questions += fetch("easy", easy_n)
    questions += fetch("medium", medium_n)
    questions += fetch("hard", hard_n)

    random.shuffle(questions)

    cur.close()
    conn.close()

    return jsonify(questions)

@app.route("/quiz/submit", methods=["POST"])
def submit_quiz():
    
    data = request.get_json()

    answers = data.get("answers", {})

    if not answers:
        return jsonify({"error": "answers required"}), 400

    conn = get_db_connection()
    cur = conn.cursor(dictionary=True)

    question_ids = list(answers.keys())

    placeholders = ",".join(["%s"] * len(question_ids))

    query = f"""
        SELECT id, correct_option, language
        FROM quiz
        WHERE id IN ({placeholders})
    """

    cur.execute(query, question_ids)

    rows = cur.fetchall()

    total = len(rows)
    score = 0

    per_language = {}

    for row in rows:
        qid = str(row["id"])
        correct = row["correct_option"]
        selected = answers.get(qid)

        if selected == correct:
            score += 1
            lang = row["language"]
            per_language[lang] = per_language.get(lang, 0) + 1

    cur.close()
    conn.close()

    return jsonify({
        "score": score,
        "total": total,
        "per_language_correct": per_language
    })

if __name__ == "__main__":
    print(app.url_map)
    app.run(debug=True)