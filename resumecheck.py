import pdfplumber
import re
import sys
from typing import List, Dict, Set

# ==========================================
# 0. GLOBAL STORAGE (The Change You Asked For)
# ==========================================
# This variable will hold the JD for the entire session
GLOBAL_JD = ""

def set_global_jd(text: str):
    """Call this function from your Web/Flask app to update the JD once."""
    global GLOBAL_JD
    GLOBAL_JD = text
    print(f"✅ Global Job Description Updated! (Length: {len(text)} chars)")

# ==========================================
# 1. THE BRAIN: Skill Ontology (Expanded)
# ==========================================
class SkillOntology:
    def __init__(self):
        self.knowledge_base = {
            # --- CORE ---
            "python": {"variations": ["python", "python3", "py"], "implies": []},
            "java": {"variations": ["java", "jdk", "j2ee"], "implies": ["oop"]},
            "cpp": {"variations": ["c++", "cpp"], "implies": ["oop"]},
            "javascript": {"variations": ["javascript", "js", "es6", "node", "nodejs"], "implies": []},
            "sql": {"variations": ["sql", "mysql", "postgres", "database"], "implies": []},

            # --- WEB ---
            "html": {"variations": ["html", "html5"], "implies": []},
            "css": {"variations": ["css", "css3", "bootstrap", "tailwind"], "implies": []},
            "react": {"variations": ["react", "reactjs", "react.js"], "implies": ["javascript", "html", "css"]},
            "angular": {"variations": ["angular", "angularjs"], "implies": ["javascript", "typescript", "html"]},
            "django": {"variations": ["django", "drf"], "implies": ["python", "sql"]},
            "node": {"variations": ["node.js", "express"], "implies": ["javascript"]},

            # --- DATA & AI ---
            "web_developer": {"variations": ["frontend", "backend "], "implies": ["javascript", "html","css"]},
            "machine_learning": {"variations": ["machine learning", "ml", "scikit-learn"], "implies": ["python", "statistics"]},
            "deep_learning": {"variations": ["deep learning", "neural networks", "pytorch", "tensorflow"], "implies": ["machine_learning", "python"]},
            
            # --- DEVOPS & CLOUD ---
            "aws": {"variations": ["aws", "amazon web services", "ec2"], "implies": ["linux"]},
            "docker": {"variations": ["docker", "containerization"], "implies": ["linux"]},
            "kubernetes": {"variations": ["kubernetes", "k8s"], "implies": ["docker", "linux"]},
            "linux": {"variations": ["linux", "bash", "shell"], "implies": []},
            
            # --- MOBILE ---
            "flutter": {"variations": ["flutter", "dart"], "implies": ["mobile_dev"]},
            "react_native": {"variations": ["react native"], "implies": ["react", "javascript"]},
            "swift": {"variations": ["swift", "ios"], "implies": ["mobile_dev"]},
        }

    def normalize_skill(self, text_token: str) -> str:
        text_token = text_token.lower().strip()
        for skill_id, data in self.knowledge_base.items():
            if text_token == skill_id or text_token in data['variations']:
                return skill_id
        return None

    def get_inferred_skills(self, found_skills: Set[str]) -> Set[str]:
        inferred = set()
        for skill in found_skills:
            if skill in self.knowledge_base:
                inferred.update(self.knowledge_base[skill].get('implies', []))
        return inferred

# ==========================================
# 2. THE ENGINE: Extraction & Logic
# ==========================================
class ResumeAnalyzer:
    def __init__(self):
        self.ontology = SkillOntology()

    def extract_text_from_pdf(self, pdf_path):
        # NOTE: When using with Flask, 'pdf_path' might be a FileStorage object
        # For now, we keep logic for file path string
        text = ""
        try:
            with pdfplumber.open(pdf_path) as pdf:
                if not pdf.pages: return "ERROR_EMPTY"
                for page in pdf.pages:
                    extracted = page.extract_text()
                    if extracted: text += extracted + "\n"
        except Exception as e:
            return f"ERROR_PARSING: {str(e)}"
        return text

    def extract_skills(self, text: str) -> Set[str]:
        found_skills = set()
        clean_text = re.sub(r'[^\w\s]', ' ', text.lower())
        tokens = clean_text.split()

        for token in tokens:
            match = self.ontology.normalize_skill(token)
            if match: found_skills.add(match)
        
        if "machine learning" in clean_text: found_skills.add("machine_learning")
        if "react native" in clean_text: found_skills.add("react_native")
        if "deep learning" in clean_text: found_skills.add("deep_learning")

        inferred = self.ontology.get_inferred_skills(found_skills)
        found_skills.update(inferred)
        
        return found_skills

    # UPDATED: jd_text is now optional (defaults to None)
    def analyze(self, pdf_path, jd_text=None):
        # 1. Handle Global JD Logic
        if jd_text is None:
            # If no JD passed, use the GLOBAL one
            if not GLOBAL_JD:
                print("❌ Error: Global Job Description is empty. Please set it first.")
                return
            jd_text = GLOBAL_JD

        # 2. Read PDF
        resume_text = self.extract_text_from_pdf(pdf_path)
        
        if str(resume_text).startswith("ERROR"):
            print(f"❌ Error reading PDF: {resume_text}")
            return

        # 3. Extract Skills
        r_skills = self.extract_skills(resume_text)
        jd_skills = self.extract_skills(jd_text)

        if not jd_skills:
            print("⚠️  Warning: The Job Description didn't contain any technical skills we recognize.")
            return

        # 4. Match
        matches = r_skills.intersection(jd_skills)
        missing = jd_skills - r_skills
        
        # 5. Score
        score = (len(matches) / len(jd_skills)) * 100

        # Output
        print(f"\n📊 ANALYSIS RESULT FOR: {pdf_path}")
        print(f"✅ MATCH SCORE: {round(score, 1)}%")
        print(f"👍 MATCHED SKILLS: {sorted(list(matches))}")
        print(f"👎 MISSING SKILLS: {sorted(list(missing))}")
        
        return score # Return score so web app can use it

# ==========================================
# 3. MAIN EXECUTION (Updated for Testing)
# ==========================================
def get_multiline_input():
    print("Paste the Job Description below (Type 'END' on a new line to finish):")
    lines = []
    while True:
        line = input()
        if line.strip() == "END": break
        lines.append(line)
    return "\n".join(lines)

if __name__ == "__main__":
    engine = ResumeAnalyzer()
    
    print("\n--- RESUME SKILL ANALYZER ---")
    
    # 1. Ask User: Do you want to set a new Global JD?
    choice = input("Do you want to update the Global Job Description? (y/n): ").lower()
    if choice == 'y':
        new_jd = get_multiline_input()
        set_global_jd(new_jd)
    
    # 2. Get Resume PDF Path
    pdf_input = input("Enter Resume PDF filename (e.g. resume.pdf): ").strip()
    
    # 3. Run Analysis (Notice we don't pass JD here; it uses Global)
    engine.analyze(pdf_input)