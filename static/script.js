// 1. Handle File Upload Display
const fileInput = document.getElementById('resumeUpload');
const fileNameLabel = document.getElementById('fileName');

fileInput.addEventListener('change', function() {
    if (this.files && this.files.length > 0) {
        fileNameLabel.textContent = "✅ " + this.files[0].name;
        fileNameLabel.style.color = "#818cf8";
        fileNameLabel.style.borderColor = "#818cf8";
    }
});

// 2. Handle Form Submission
document.getElementById('evaluationForm').addEventListener('submit', function(e) {
    e.preventDefault(); // Stop page reload

    const jd = document.getElementById('jdInput').value;
    const github = document.getElementById('githubUrl').value;
    const comments = document.getElementById('mentorComments').value;
    const file = fileInput.files[0];

    // Validation
    if (!jd) {
        alert("⚠️ Please fill in the Job Description first!");
        return;
    }
    if (!file) {
        alert("⚠️ Please upload a Resume!");
        return;
    }

    // Show loading state
    const btn = document.querySelector('.cta-button');
    const originalText = btn.innerText;
    btn.innerText = "Processing...";
    btn.style.background = "#f58092";
    btn.disabled = true;

    // Step 1: Set Job Description
    fetch('/set_jd', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({ jd_text: jd })
    })
    .then(response => response.json())
    .then(data => {
        if (data.status === 'error') {
            throw new Error(data.message);
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
    .then(response => response.json())
    .then(data => {
        if (data.error) {
            throw new Error(data.error);
        }
        
        // Display results
        console.log("Analysis Results:", data);
        
        // If quiz is available, redirect to quiz page
        if (data.quiz && data.quiz.length > 0) {
            // Quiz will be displayed on quiz page
            window.location.href = '/quiz';
        } else {
            // No quiz generated, go directly to results
            window.location.href = '/results';
        }
    })
    .catch(error => {
        console.error("Error:", error);
        alert("❌ Error: " + error.message);
    })
    .finally(() => {
        // Reset button
        btn.innerText = originalText;
        btn.style.background = "";
        btn.disabled = false;
    });
});