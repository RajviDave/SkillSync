from flask import Flask, redirect, request, jsonify, render_template, session, url_for
import os
from werkzeug.utils import secure_filename
import random
from werkzeug.security import generate_password_hash, check_password_hash
from flask_sqlalchemy import SQLAlchemy

# Import your custom modules
from resume import resume
from comments import comments
from git import git
from domain_match import match_domain
from languages import domain_to_languages

app = Flask(__name__)
app.secret_key = "skillsync_secret"

# --- DATABASE CONFIGURATION ---
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///skillsync.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

# --- MODELS ---
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(100), unique=True, nullable=False)
    password = db.Column(db.String(200), nullable=False)
    role = db.Column(db.String(20), nullable=False)

class Quiz(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    language = db.Column(db.String(50))
    difficulty = db.Column(db.String(50))
    question = db.Column(db.String(500), nullable=False)
    optionA = db.Column(db.String(200))
    optionB = db.Column(db.String(200))
    optionC = db.Column(db.String(200))
    optionD = db.Column(db.String(200))
    correct_option = db.Column(db.String(1))

class AssessmentResult(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    student_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    job_domain = db.Column(db.String(100))
    resume_score = db.Column(db.Float)
    quiz_score = db.Column(db.Float)
    mentor_score = db.Column(db.Float)
    final_score = db.Column(db.Float)
    date_added = db.Column(db.DateTime, default=db.func.current_timestamp())

# --- ROUTES: AUTHENTICATION ---

@app.route("/")
def home():
    if 'user_id' not in session:
        return redirect(url_for("login"))
    if session.get('role') == 'mentor':
        return redirect(url_for("mentor_dashboard"))
    
    stage = session.get('assessment_stage')
    if stage == 'quiz': return redirect(url_for("quiz_page"))
    elif stage == 'result': return redirect(url_for("result_page"))
    
    return render_template("input_form.html", user_name=session.get('user_name'))

@app.route("/signup", methods=["GET", "POST"])
def signup():
    if 'user_id' in session: return redirect("/")
    if request.method == "POST":
        hashed_pw = generate_password_hash(request.form['password'], method='pbkdf2:sha256')
        new_user = User(
            name=request.form['name'],
            email=request.form['email'],
            password=hashed_pw,
            role=request.form['role']
        )
        try:
            db.session.add(new_user)
            db.session.commit()
            return redirect(url_for("login"))
        except Exception as e:
            db.session.rollback()
            return f"Error: {e}"
    return render_template("signup.html")

@app.route("/login", methods=["GET", "POST"])
def login():
    if 'user_id' in session: return redirect("/")
    if request.method == "POST":
        email = request.form['email']
        password = request.form['password']
        user = User.query.filter_by(email=email).first()
        if user and check_password_hash(user.password, password):
            session.update({'user_id': user.id, 'user_name': user.name, 'role': user.role})
            return redirect(url_for("mentor_dashboard") if user.role == 'mentor' else "/")
        return "Invalid Credentials"
    return render_template("login.html")

@app.route("/logout")
def logout():
    session.clear()
    return redirect(url_for("login"))

# --- ROUTES: MENTOR DASHBOARD ---

@app.route("/mentor_dashboard")
def mentor_dashboard():
    if session.get('role') != 'mentor': return "Access Denied", 403
    search_query = request.args.get('search', '').strip()
    
    query = db.session.query(User.name, AssessmentResult).join(AssessmentResult, User.id == AssessmentResult.student_id)
    if search_query:
        query = query.filter(User.name.contains(search_query))
    
    results = query.order_by(AssessmentResult.date_added.desc()).all()
    return render_template("mentor_dashboard.html", students=results, last_search=search_query)

# --- ROUTES: STUDENT ASSESSMENT ---

@app.route("/analyze", methods=["POST"])
def analyze():
    if session.get('role') != 'student': return "Access Denied"
    
    # Simple File Save
    resume_file = request.files.get("resume")
    UPLOAD_FOLDER = "uploads"
    os.makedirs(UPLOAD_FOLDER, exist_ok=True)
    resume_path = os.path.join(UPLOAD_FOLDER, secure_filename(resume_file.filename))
    resume_file.save(resume_path)

    # Logic
    jd_domains = match_domain(request.form.get("jd"))
    domain_name = list(jd_domains.keys())[0] if jd_domains else "General"
    resume_results = resume(resume_path, jd_domains)
    
    # Score Calc
    total_r = sum(int(s.split('/')[0]) for s in resume_results.values() if '/' in s)
    avg_resume = total_r / len(resume_results) if resume_results else 0
    
    session.update({
        'current_domain': domain_name,
        'resume_score_numeric': avg_resume,
        'mentor_score': comments(request.form.get("comments")),
        'quiz_languages': git(request.form.get("git"), jd_domains) or ["Python"],
        'assessment_stage': 'quiz'
    })
    return redirect(url_for("quiz_page"))

@app.route("/quiz")
def quiz_page():
    if session.get('assessment_stage') == 'result': return redirect(url_for("result_page"))
    langs = session.get("quiz_languages", ["Python"])
    # Randomly select 15 questions for the languages
    questions = Quiz.query.filter(Quiz.language.in_(langs)).order_by(db.func.random()).limit(15).all()
    return render_template("quiz.html", questions=questions)

@app.route("/quiz/submit", methods=["POST"])
def submit_quiz():
    answers = request.form.to_dict()
    score = 0
    total = 0
    for k, user_ans in answers.items():
        qid = int(k.replace("answers[", "").replace("]", ""))
        q = Quiz.query.get(qid)
        if q and q.correct_option == user_ans: score += 1
        total += 1

    quiz_pct = (score / total * 100) if total > 0 else 0
    res_score = session.get('resume_score_numeric', 0)
    men_score = session.get('mentor_score', 50)
    final = round((res_score * 0.3) + (quiz_pct * 0.5) + (men_score * 0.2), 2)

    # Save to SQLite
    res = AssessmentResult(
        student_id=session.get('user_id'),
        job_domain=session.get('current_domain'),
        resume_score=res_score,
        quiz_score=quiz_pct,
        mentor_score=men_score,
        final_score=final
    )
    db.session.add(res)
    db.session.commit()

    session['final_results'] = {'score': score, 'total': total, 'final_score': final}
    session['assessment_stage'] = 'result'
    return redirect(url_for("result_page"))

@app.route("/result")
def result_page():
    if session.get('assessment_stage') != 'result': return redirect("/")
    return render_template("result.html", **session.get('final_results'))

if __name__ == "__main__":
    with app.app_context():
        db.create_all()
    
    # This line tells Flask to use Render's port
    port = int(os.environ.get("PORT", 10000))
    app.run(host='0.0.0.0', port=port)