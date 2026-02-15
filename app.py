from flask import Flask, redirect, request, jsonify, render_template, session, url_for
import os
from werkzeug.utils import secure_filename
import mysql.connector
import random

# Import your custom modules
from resume import resume
from comments import comments
from git import git
from domain_match import match_domain
from languages import domain_to_languages

app = Flask(__name__)
app.secret_key = "skillsync_secret"

# --- DATABASE CONNECTION ---
def get_db_connection():
    return mysql.connector.connect(
        host="localhost",
        user="root",
        password="",
        database="auth_system"
    )

# --- ROUTES: AUTHENTICATION ---

@app.route("/")
def home():
    # If not logged in, go to login
    if 'user_id' not in session:
        return redirect("/login")
    
    # If Mentor, go to Dashboard
    if session.get('role') == 'mentor':
        return redirect("/mentor/dashboard")
    
    # If Student, go to Input Form
    return render_template("input_form.html", user_name=session.get('user_name'))

@app.route("/signup", methods=["GET", "POST"])
def signup():
    if request.method == "POST":
        name = request.form['name']
        email = request.form['email']
        password = request.form['password']
        role = request.form['role'] # 'student' or 'mentor'

        conn = get_db_connection()
        cur = conn.cursor()
        try:
            cur.execute("INSERT INTO users (name, email, password, role) VALUES (%s, %s, %s, %s)", 
                        (name, email, password, role))
            conn.commit()
            return redirect("/login")
        except Exception as e:
            return f"Error: {e}"
        finally:
            cur.close()
            conn.close()

    return render_template("signup.html")

@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        email = request.form['email']
        password = request.form['password']

        conn = get_db_connection()
        cur = conn.cursor(dictionary=True)
        cur.execute("SELECT * FROM users WHERE email=%s AND password=%s", (email, password))
        user = cur.fetchone()
        cur.close()
        conn.close()

        if user:
            session['user_id'] = user['id']
            session['user_name'] = user['name']
            session['role'] = user['role']
            
            if user['role'] == 'mentor':
                return redirect("/mentor/dashboard")
            else:
                return redirect("/")
        else:
            return "Invalid Credentials"

    return render_template("login.html")

@app.route("/logout")
def logout():
    session.clear()
    return redirect("/login")

# --- ROUTES: MENTOR DASHBOARD ---

@app.route("/mentor/dashboard")
def mentor_dashboard():
    # Security Check
    if session.get('role') != 'mentor':
        return "Access Denied: Mentors Only"

    conn = get_db_connection()
    cur = conn.cursor(dictionary=True)
    
    # Fetch all results joined with user names
    query = """
        SELECT users.name, ar.job_domain, ar.resume_score, ar.quiz_score, 
               ar.mentor_score, ar.final_score, ar.date_added
        FROM assessment_results ar
        JOIN users ON ar.student_id = users.id
        ORDER BY ar.date_added DESC
    """
    cur.execute(query)
    results = cur.fetchall()
    
    cur.close()
    conn.close()

    return render_template("mentor_dashboard.html", students=results)

# --- ROUTES: STUDENT ASSESSMENT FLOW ---

# FIX: Renamed back to "/analyze" to match your HTML form action
@app.route("/analyze", methods=["POST"])
def analyze():
    if session.get('role') != 'student':
        return "Access Denied"

    job_description = request.form.get("jd")
    resume_file = request.files.get("resume")
    mentor_comments = request.form.get("comments")
    github_username = request.form.get("git")

    UPLOAD_FOLDER = "uploads"
    os.makedirs(UPLOAD_FOLDER, exist_ok=True)
    filename = secure_filename(resume_file.filename)
    resume_path = os.path.join(UPLOAD_FOLDER, filename)
    resume_file.save(resume_path)

    # 1. Identify Domain
    jd_domains = match_domain(job_description)
    # Convert dict keys to string for storage/display (e.g., "Web Development")
    domain_name = list(jd_domains.keys())[0] if jd_domains else "General"
    session['current_domain'] = domain_name

    # 2. Analyze Resume
    resume_results = resume(resume_path, jd_domains)
    
    # Calculate Numeric Resume Score
    total_r = 0
    count_r = 0
    for d, s in resume_results.items():
        try:
            total_r += int(s.split('/')[0])
            count_r += 1
        except: continue
    avg_resume_score = total_r / count_r if count_r > 0 else 0
    session['resume_score_numeric'] = avg_resume_score

    # 3. Analyze Comments (Sentiment)
    mentor_score = comments(mentor_comments)
    session['mentor_score'] = mentor_score

    # 4. GitHub & Quiz Setup (Fallback Logic)
    github_results = git(github_username, jd_domains)
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
    if not languages: return "No quiz generated."
    
    conn = get_db_connection()
    cur = conn.cursor(dictionary=True)
    
    # Dynamically handle multiple languages
    placeholders = ",".join(["%s"] * len(languages))
    query = f"SELECT * FROM quiz WHERE language IN ({placeholders}) ORDER BY RAND() LIMIT 15"
    
    # Pass languages tuple to execute
    cur.execute(query, tuple(languages))
    questions = cur.fetchall()
    cur.close()
    conn.close()
    
    return render_template("quiz.html", questions=questions)

@app.route("/quiz/submit", methods=["POST"])
def submit_quiz():
    answers = request.form.to_dict()
    clean = {int(k.replace("answers[", "").replace("]", "")): v for k, v in answers.items()}

    score = 0
    total = len(clean)
    conn = get_db_connection()
    cur = conn.cursor(dictionary=True)
    
    for qid, user_ans in clean.items():
        cur.execute("SELECT correct_option FROM quiz WHERE id=%s", (qid,))
        row = cur.fetchone()
        if row and row['correct_option'] == user_ans:
            score += 1

    # --- FINAL CALCULATION ---
    quiz_percentage = (score / total * 100) if total > 0 else 0
    resume_score = session.get('resume_score_numeric', 0)
    mentor_score = session.get('mentor_score', 50)
    
    final_score = (resume_score * 0.30) + (quiz_percentage * 0.50) + (mentor_score * 0.20)
    final_score = round(final_score, 2)

    # --- SAVE TO DATABASE ---
    student_id = session.get('user_id')
    current_domain = session.get('current_domain', 'Unknown')

    cur.execute("""
        INSERT INTO assessment_results 
        (student_id, job_domain, resume_score, quiz_score, mentor_score, final_score)
        VALUES (%s, %s, %s, %s, %s, %s)
    """, (student_id, current_domain, resume_score, quiz_percentage, mentor_score, final_score))
    
    conn.commit()
    cur.close()
    conn.close()

    return render_template("result.html", 
                           final_score=final_score, 
                           resume_score=resume_score,
                           quiz_percentage=quiz_percentage,
                           mentor_score=mentor_score,
                           score=score, total=total)

if __name__ == "__main__":
    app.run(debug=True)