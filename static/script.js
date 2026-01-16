// Wait for DOM to be fully loaded
document.addEventListener('DOMContentLoaded', function() {
    // 1. Handle File Upload Display (if elements exist)
    const fileInput = document.getElementById('resumeUpload');
    const fileNameLabel = document.getElementById('fileName');

    if (fileInput && fileNameLabel) {
        fileInput.addEventListener('change', function() {
            if (this.files && this.files.length > 0) {
                fileNameLabel.textContent = "✅ " + this.files[0].name;
                fileNameLabel.style.color = "#818cf8";
            }
        });
    }

    // 2. Handle Form Submission (if form exists)
    const evaluationForm = document.getElementById('evaluationForm');
    if (evaluationForm) {
        evaluationForm.addEventListener('submit', function(e) {
            e.preventDefault(); // Stop page reload

            const jd = document.getElementById('jdInput').value.trim();
            const github = document.getElementById('githubUrl').value.trim();
            const comments = document.getElementById('mentorComments').value.trim();
            const file = fileInput ? fileInput.files[0] : null;

            // Validation
            if (!jd) {
                alert("⚠️ Please fill in the Job Description first!");
                document.getElementById('jdInput').focus();
                return;
            }
            if (!file) {
                alert("⚠️ Please upload a Resume (PDF file)!");
                if (fileInput) fileInput.focus();
                return;
            }

            // Show loading state
            const btn = document.getElementById('submitBtn') || document.querySelector('.cta-button');
            if (!btn) return;
            
            const originalText = btn.innerText;
            btn.innerText = "⏳ Processing...";
            btn.disabled = true;

            // Step 1: Set Job Description
            fetch('/set_jd', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({ jd_text: jd })
            })
            .then(response => {
                if (!response.ok) {
                    throw new Error('Network response was not ok');
                }
                return response.json();
            })
            .then(data => {
                if (data.status === 'error') {
                    throw new Error(data.message || 'Failed to set job description');
                }
                
                // Step 2: Prepare form data for analysis
                const formData = new FormData();
                formData.append('resume', file);
                formData.append('comments', comments);
                formData.append('github', github);
                
                // Extract username from GitHub URL if provided, or use as-is if it's just a username
                if (github) {
                    let username = github.trim();
                    // Check if it's a URL
                    const githubMatch = github.match(/github\.com\/([^\/]+)/);
                    if (githubMatch) {
                        username = githubMatch[1];
                    } else if (!github.includes('/') && !github.includes('http')) {
                        // It's likely just a username
                        username = github;
                    }
                    if (username) {
                        formData.append('github_username', username);
                    }
                }
                
                // Step 3: Submit for analysis
                return fetch('/analyze', {
                    method: 'POST',
                    body: formData
                });
            })
            .then(response => {
                if (!response.ok) {
                    throw new Error('Network response was not ok');
                }
                return response.json();
            })
            .then(data => {
                if (data.error) {
                    throw new Error(data.error);
                }
                
                // Display results
                console.log("Analysis Results:", data);
                
                // If quiz is available, redirect to quiz page
                if (data.quiz && data.quiz.length > 0) {
                    // Quiz will be displayed on quiz page
                    btn.innerText = "✅ Redirecting to Quiz...";
                    setTimeout(() => {
                        window.location.href = '/quiz';
                    }, 500);
                } else {
                    // No quiz generated, go directly to results
                    btn.innerText = "✅ Redirecting to Results...";
                    setTimeout(() => {
                        window.location.href = '/results';
                    }, 500);
                }
            })
            .catch(error => {
                console.error("Error:", error);
                alert("❌ Error: " + error.message);
                // Reset button
                btn.innerText = originalText;
                btn.disabled = false;
            });
        });
    }
});