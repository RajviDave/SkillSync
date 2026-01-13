import pdfplumber
import re
import sys
from typing import List, Dict, Set

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
        """Standardizes skills (e.g. 'react.js' -> 'react')"""
        text_token = text_token.lower().strip()
        for skill_id, data in self.knowledge_base.items():
            if text_token == skill_id or text_token in data['variations']:
                return skill_id
        return None

    def get_inferred_skills(self, found_skills: Set[str]) -> Set[str]:
        """If user has 'React', add 'JavaScript' automatically."""
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

    def extract_text_from_pdf(self, pdf_path: str) -> str:
        text = ""
        try:
            with pdfplumber.open(pdf_path) as pdf:
                if not pdf.pages: return "ERROR_EMPTY"
                for page in pdf.pages:
                    extracted = page.extract_text()
                    if extracted: text += extracted + "\n"
        except FileNotFoundError:
            return "ERROR_NOT_FOUND"
        except Exception as e:
            return f"ERROR_PARSING: {str(e)}"
        return text

    def extract_skills(self, text: str) -> Set[str]:
        found_skills = set()
        # Clean text: lowercase and remove punctuation
        clean_text = re.sub(r'[^\w\s]', ' ', text.lower())
        tokens = clean_text.split()

        # 1. Check every word against dictionary
        for token in tokens:
            match = self.ontology.normalize_skill(token)
            if match: found_skills.add(match)
        
        # 2. Check specific multi-word phrases (Manual addition for safety)
        if "machine learning" in clean_text: found_skills.add("machine_learning")
        if "react native" in clean_text: found_skills.add("react_native")
        if "deep learning" in clean_text: found_skills.add("deep_learning")

        # 3. Add Inferred Skills (The "Brain" part)
        inferred = self.ontology.get_inferred_skills(found_skills)
        found_skills.update(inferred)
        
        return found_skills

    def analyze(self, pdf_path: str, jd_text: str):
        # 1. Read PDF
        resume_text = self.extract_text_from_pdf(pdf_path)
        
        if resume_text == "ERROR_NOT_FOUND":
            print(f"❌ Error: File '{pdf_path}' not found.")
            return
        if resume_text.startswith("ERROR"):
            print(f"❌ Error reading PDF: {resume_text}")
            return

        # 2. Extract Skills
        r_skills = self.extract_skills(resume_text)
        jd_skills = self.extract_skills(jd_text)

        if not jd_skills:
            print("⚠️  Warning: The Job Description didn't contain any technical skills we recognize.")
            return

        # 3. Match
        matches = r_skills.intersection(jd_skills)
        missing = jd_skills - r_skills
        
        # 4. Score (Percentage Match)
        score = (len(matches) / len(jd_skills)) * 100

        # 5. Output Results
        print("\n" + "="*40)
        print(f"📊 ANALYSIS RESULT FOR: {pdf_path}")
        print("="*40)
        print(f"✅  MATCH SCORE: {round(score, 1)}%")
        print("-" * 20)
        print(f"Found in Resume: {sorted(list(r_skills))}")
        print(f"Required by JD:  {sorted(list(jd_skills))}")
        print("-" * 20)
        print(f"👍 MATCHED SKILLS: {sorted(list(matches))}")
        print(f"👎 MISSING SKILLS: {sorted(list(missing))}")
        print("="*40)

# ==========================================
# 3. MAIN EXECUTION
# ==========================================
def get_multiline_input():
    print("Paste the Job Description below (Type 'END' on a new line to finish):")
    lines = []
    while True:
        line = input()
        if line.strip() == "END":
            break
        lines.append(line)
    return "\n".join(lines)

if __name__ == "__main__":
    engine = ResumeAnalyzer()
    
    print("\n--- RESUME SKILL ANALYZER ---")
    
    # 1. Get Resume PDF Path
    pdf_input = input("Enter Resume PDF filename (e.g. resume.pdf): ").strip()
    
    # 2. Get JD String
    jd_input = get_multiline_input()
    
    # 3. Run
    engine.analyze(pdf_input, jd_input)