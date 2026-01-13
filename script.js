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

// 2. Handle Form Submission (Simulation)
document.getElementById('evaluationForm').addEventListener('submit', function(e) {
    e.preventDefault(); // Stop page reload

    const jd = document.getElementById('jdInput').value;
    const github = document.getElementById('githubUrl').value;
    const comments = document.getElementById('mentorComments').value;
    const file = fileInput.files[0];

    // Simple Validation for Demo
    if (!jd) {
        alert("⚠️ Please fill in the Job Description first!");
        return;
    }
    if (!file) {
        alert("⚠️ Please upload a Resume!");
        return;
    }

    console.log("--- SUBMITTING DATA ---");
    console.log("JD:", jd);
    console.log("GitHub:", github);
    console.log("Comments:", comments);
    console.log("File:", file.name);

    // Show Success Animation/Alert
    const btn = document.querySelector('.cta-button');
    const originalText = btn.innerText;
    
    btn.innerText = "Processing...";
    btn.style.background = "#f58092"; // Change to Pink on loading

    setTimeout(() => {
        alert("Data Captured! (Ready for Python Backend)");
        btn.innerText = originalText;
        btn.style.background = ""; // Reset
    }, 1000);
});