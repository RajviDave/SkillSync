from flask import Flask, request, jsonify, render_template
import os
from werkzeug.utils import secure_filename
from resume import resume
from comments import comments
from git import git
from domain_match import match_domain

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

if __name__ == "__main__":
    app.run(debug=True)
