from flask import Flask, redirect, request, jsonify, render_template
import os
from werkzeug.utils import secure_filename
from resume import resume
from comments import comments
from git import git
from domain_match import match_domain
import mysql.connector
import random
from flask import session
from languages import domain_to_languages

app = Flask(__name__)

app.secret_key = "skillsync_secret"

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
    
    # CHANGE THIS LINE: Instead of jsonify, use render_template
    return render_template(
        "analysis_result.html",       # The HTML file you want to show
        resume_scores=resume_results, # Passing the resume score dict
        mentor_feedback=comments_results,
        git_data=github_results
    )

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
    
    answers = request.form.to_dict()

    # Normalize keys
    clean = {}
    for k, v in answers.items():
        qid = k.replace("answers[", "").replace("]", "")
        clean[int(qid)] = v

    score = 0
    total = len(clean)

    conn = get_db_connection()
    cur = conn.cursor(dictionary=True)

    for qid, user_ans in clean.items():
        cur.execute("SELECT correct_option FROM quiz WHERE id=%s", (qid,))
        row = cur.fetchone()
        if row and row["correct_option"] == user_ans:
            score += 1

    cur.close()
    conn.close()

    # --- NEW LOGIC: Calculate Final Weighted Score ---
    
    # 1. Calculate Quiz Percentage (e.g., 10/15 -> 66.6%)
    if total > 0:
        quiz_percentage = (score / total) * 100
    else:
        quiz_percentage = 0

    # 2. Retrieve Resume Score from Session (Default to 0 if missing)
    resume_score = session.get('resume_score_numeric', 0)
    mentor_score = session.get('mentor_score', 50)

    # 3. Apply Weights (30% Resume, 70% Quiz)
    final_weighted_score = (
        (resume_score * 0.30) + 
        (quiz_percentage * 0.50) + 
        (mentor_score * 0.20)
    )

    # Round for display
    final_weighted_score = round(final_weighted_score, 2)
    resume_score = round(resume_score, 2)
    mentor_Score=round(mentor_score,2)
    quiz_percentage = round(quiz_percentage, 2)

    return render_template(
        "result.html",
        score=score,                # Raw quiz score (e.g., 10)
        total=total,                # Total questions (e.g., 15)
        resume_score=resume_score,  # Resume % (e.g., 60.0)
        quiz_percentage=quiz_percentage, # Quiz % (e.g., 66.6)
        mentor_score=mentor_score,
        final_score=final_weighted_score # Final Weighted Score
    )
    
@app.route("/analyze", methods=["POST"])
def analyze():
    resume_file = request.files["resume"]
    jd = request.form["jd"]
    comments_text = request.form.get("comments", "")
    github_username = request.form.get("git", "")

    os.makedirs("uploads", exist_ok=True)
    resume_path = os.path.join("uploads", resume_file.filename)
    resume_file.save(resume_path)

    # 1. Identify Domains
    jd_domains = match_domain(jd)

    # 2. Get Resume Scores (Returns dict like {'Web Dev': '60/100'})
    resume_results = resume(resume_path, jd_domains)
    
    # --- NEW LOGIC: Calculate Average Resume Score ---
    total_resume_score = 0
    count = 0
    
    for domain, score_str in resume_results.items():
        # score_str is "60/100", we need just 60
        try:
            numeric_score = int(score_str.split('/')[0])
            total_resume_score += numeric_score
            count += 1
        except:
            continue
            
    # Avoid division by zero
    avg_resume_score = total_resume_score / count if count > 0 else 0
    
    # SAVE TO SESSION for later use
    session['resume_score_numeric'] = avg_resume_score
    # -------------------------------------------------

    # 2. Get Mentor Comment Score (NEW)
    comments_text = request.form.get("comments", "")
    mentor_score = comments(comments_text) # Returns integer 0-100
    session['mentor_score'] = mentor_score # Save to session

    # 3. Get GitHub Data (Your existing logic)
    github_results = git(github_username, jd_domains)
    
    # Fallback logic for quiz languages
    if not github_results:
        fallback_set = set()
        iterable = jd_domains.keys() if isinstance(jd_domains, dict) else jd_domains
        for domain in iterable:
            if domain in domain_to_languages:
                for lang in domain_to_languages[domain]:
                    fallback_set.add(lang)
        github_results = list(fallback_set)

    session["quiz_languages"] = github_results

    return redirect("/quiz")

@app.route("/quiz")
def quiz_page():

    languages = session.get("quiz_languages", [])
    languages = list(languages)
    languages = [l for l in languages if isinstance(l, str)]

    print("SESSION LANGUAGES =", languages)

    if not languages:
        return "No quiz languages found in session"

    total = 15

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

    print("TOTAL QUESTIONS =", len(questions))

    cur.close()
    conn.close()

    random.shuffle(questions)

    return render_template("quiz.html", questions=questions)

if __name__ == "__main__":
    print(app.url_map)
    app.run(debug=True)