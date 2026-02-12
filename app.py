from flask import Flask, request, jsonify, render_template

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

    if not job_description or not resume_file or not mentor_comments or not github_username:
        return "Missing input", 400

    if resume_file.mimetype != "application/pdf":
        return "Only PDF files are allowed", 400

    # TEMP: just to prove data is coming
    return jsonify({
        "jd": job_description,
        "resume_filename": resume_file.filename,
        "comments":mentor_comments,
        "github": github_username,
        
    })


if __name__ == "__main__":
    app.run(debug=True)
