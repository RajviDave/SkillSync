from flask import Flask, render_template, request, jsonify, session, redirect, url_for
from resumecheck import ResumeAnalyzer, set_global_jd, GLOBAL_JD
from comments import FeedbackComponent
from github_integration import generate_quiz_from_github, calculate_github_score
import os
import subprocess
import json as json_lib

app = Flask(__name__, template_folder='templates', static_folder='.')
app.secret_key = os.urandom(24)  # Required for Flask sessions

# --- HELPER FUNCTIONS ---

def check_php_session():
    """Check if user is authenticated via PHP session"""
    try:
        # Use the check_session.php file
        result = subprocess.run(
            ['php', 'backend/check_session.php'],
            capture_output=True,
            text=True,
            cwd=os.path.dirname(os.path.abspath(__file__))
        )
        if result.returncode == 0:
            return json_lib.loads(result.stdout)
    except Exception as e:
        print(f"Error checking PHP session: {e}")
    return {"authenticated": False}

# --- ROUTES ---

@app.route('/')
def home():
    # Check if user is authenticated
    auth_status = check_php_session()
    if auth_status.get("authenticated"):
        return redirect(url_for('main_page'))
    # Serve landing page
    return render_template('index.html')

@app.route('/auth')
def auth_page():
    """Authentication page"""
    return render_template('auth.html') if os.path.exists('templates/auth.html') else open('auth.html').read()

@app.route('/main')
def main_page():
    """Main evaluation form page"""
    # Check authentication
    auth_status = check_php_session()
    if not auth_status.get("authenticated"):
        return redirect(url_for('auth_page'))
    
    return render_template('main.html', user=auth_status.get("user", {}))

@app.route('/generate_quiz', methods=['POST'])
def generate_quiz():
    """Generate quiz from GitHub username and job description"""
    data = request.json
    github_username = data.get('github_username', "")
    jd_text = data.get('jd_text', GLOBAL_JD)
    
    if not github_username:
        return jsonify({"error": "GitHub username is required"})
    
    if not jd_text:
        return jsonify({"error": "Job description is required"})
    
    quiz_result = generate_quiz_from_github(jd_text, github_username)
    
    if quiz_result.get("error"):
        return jsonify({"error": quiz_result["error"]})
    
    return jsonify({
        "status": "success",
        "quiz": quiz_result["quiz"],
        "language_stats": quiz_result.get("language_stats", {})
    })

@app.route('/set_jd', methods=['POST'])
def update_global_jd():
    """Receives JD from Web and saves it globally"""
    data = request.json
    jd_text = data.get('jd_text', "")
    
    if jd_text:
        set_global_jd(jd_text)
        return jsonify({"status": "success", "message": "JD Updated Successfully!"})
    return jsonify({"status": "error", "message": "JD cannot be empty!"})

@app.route('/analyze', methods=['POST'])
def analyze_candidate():
    """Receives Resume + Comments + Github from Web"""
    
    # 1. Get Resume File
    if 'resume' not in request.files:
        return jsonify({"error": "No resume file uploaded"})
    
    file = request.files['resume']
    
    # 2. Get Comments & Github
    comments = request.form.get('comments', "")
    github_link = request.form.get('github', "")
    github_username = request.form.get('github_username', "")
    
    # Extract username from GitHub link if provided as URL
    if github_link and not github_username:
        if "github.com" in github_link:
            # Extract username from URL (e.g., https://github.com/username or https://github.com/username/repo)
            parts = github_link.replace("https://github.com/", "").replace("http://github.com/", "").strip("/").split("/")
            if parts and parts[0]:
                github_username = parts[0]
        else:
            # Assume it's just a username
            github_username = github_link.strip()

    # Check if JD is set
    if not GLOBAL_JD:
        return jsonify({"error": "Job Description not set. Please set JD first using /set_jd endpoint."})
    
    # 3. RUN RESUME ANALYSIS (Using your logic.py)
    # We pass the file stream directly to your engine
    engine = ResumeAnalyzer()
    
    # Note: We don't pass JD here because logic.py uses GLOBAL_JD automatically
    # But we need to make sure logic.py can read a file stream, not just a path.
    # (Your extract_text_from_pdf handles pdfplumber.open(file) automatically usually)
    try:
        # Calculate Resume Score (0-100)
        raw_resume_score = engine.analyze(file)
        
        # If analyze returned None (error), set to 0
        if raw_resume_score is None: raw_resume_score = 0
        
        # Weighted Resume Score (20%)
        resume_weighted = (raw_resume_score / 100) * 20
        
    except Exception as e:
        return jsonify({"error": f"Resume processing failed: {str(e)}"})

    # 4. RUN FEEDBACK ANALYSIS (30%)
    feedback_score = 0
    if comments:
        feedback_engine = FeedbackComponent()
        # Convert single comment string to list format expected by FeedbackComponent
        comments_list = [comments] if comments else []
        feedback_score = feedback_engine.get_score(comments_list)

    # 5. RUN GITHUB ANALYSIS (50%)
    github_score = 0
    quiz_data = None
    if github_username:
        # Calculate score based on repository analysis
        github_score = calculate_github_score(github_username, GLOBAL_JD)
        
        # Generate quiz from GitHub data
        quiz_result = generate_quiz_from_github(GLOBAL_JD, github_username)
        if quiz_result.get("quiz"):
            quiz_data = quiz_result["quiz"] 

    # 6. TOTAL
    total = resume_weighted + feedback_score + github_score

    response_data = {
        "total_score": round(total, 2),
        "breakdown": {
            "resume": round(resume_weighted, 2),
            "feedback": round(feedback_score, 2),
            "github": round(github_score, 2)
        }
    }
    
    # Add quiz data if available
    if quiz_data:
        response_data["quiz"] = quiz_data
        # Store in session for quiz page
        session['quiz_data'] = quiz_data
        session['analysis_results'] = {
            "total_score": round(total, 2),
            "breakdown": response_data["breakdown"]
        }
    
    return jsonify(response_data)

@app.route('/quiz')
def quiz_page():
    """Quiz display page"""
    # Check authentication
    auth_status = check_php_session()
    if not auth_status.get("authenticated"):
        return redirect(url_for('auth_page'))
    
    # Get quiz from session
    quiz_data = session.get('quiz_data')
    if not quiz_data:
        return redirect(url_for('main_page'))
    
    return render_template('quiz.html', quiz=quiz_data)

@app.route('/submit_quiz', methods=['POST'])
def submit_quiz():
    """Submit quiz answers and calculate score"""
    data = request.json
    answers = data.get('answers', {})
    quiz_data = session.get('quiz_data', [])
    
    if not quiz_data:
        return jsonify({"error": "No quiz data found"})
    
    # Calculate score
    correct = 0
    total = len(quiz_data)
    
    for i, question in enumerate(quiz_data):
        user_answer = answers.get(str(i), "")
        correct_answer = question.get('correct_option', '')
        if user_answer.upper() == correct_answer.upper():
            correct += 1
    
    quiz_score = (correct / total) * 100 if total > 0 else 0
    
    # Store quiz results in session
    session['quiz_results'] = {
        "score": round(quiz_score, 2),
        "correct": correct,
        "total": total
    }
    
    return jsonify({
        "status": "success",
        "score": round(quiz_score, 2),
        "correct": correct,
        "total": total
    })

@app.route('/results')
def results_page():
    """Final results page"""
    # Check authentication
    auth_status = check_php_session()
    if not auth_status.get("authenticated"):
        return redirect(url_for('auth_page'))
    
    # Get all results from session
    analysis_results = session.get('analysis_results', {})
    quiz_results = session.get('quiz_results', {})
    
    if not analysis_results:
        return redirect(url_for('main_page'))
    
    return render_template('results.html', 
                         analysis=analysis_results,
                         quiz=quiz_results)

if __name__ == '__main__':
    app.run(debug=True)