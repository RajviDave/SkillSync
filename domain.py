import re

abbr_map = {

# ---------- AI / ML / DS ----------
"ml": "machine learning",
"ai": "artificial intelligence",
"dl": "deep learning",
"cv": "computer vision",
"nlp": "natural language processing",
"llm": "large language model",
"genai": "generative ai",
"gen ai": "generative ai",
"rl": "reinforcement learning",
"mlops": "machine learning operations",

# ---------- Data ----------
"bi": "business intelligence",
"eda": "exploratory data analysis",
"etl": "extract transform load",
"elt": "extract load transform",

# ---------- Cloud / DevOps ----------
"ci/cd": "ci cd",
"ci-cd": "ci cd",
"iac": "infrastructure as code",
"sre": "site reliability engineering",

# ---------- Web / App ----------
"fe": "frontend",
"be": "backend",
"ui": "user interface",
"ux": "user experience",
"spa": "single page application",
"pwa": "progressive web application",

# ---------- Mobile ----------
"rn": "react native",

# ---------- Security ----------
"soc": "security operations center",
"iam": "identity and access management",

# ---------- AR / VR / XR ----------
"ar": "augmented reality",
"vr": "virtual reality",
"mr": "mixed reality",
"xr": "extended reality",

# ---------- Embedded / IoT ----------
"mcu": "microcontroller",
"rtos": "real time operating system",
"bsp": "board support package",

# ---------- VLSI / Hardware ----------
"asic": "application specific integrated circuit",
"fpga": "field programmable gate array",
"rtl": "register transfer level",
"sta": "static timing analysis",
"dft": "design for testability",
"pd": "physical design",

# ---------- General ----------
"api": "api",   # keeps api consistent
"rest": "rest",
"oop": "object oriented programming",
"os": "operating system"
}

domain_keywords = {

    "embedded_systems": [
    "embedded","firmware","microcontroller","rtos","bare metal",
    "arm cortex","stm32","esp32","arduino","raspberry pi",
    "spi","i2c","uart","can bus","device driver","board bringup"
    ],

    "vlsi": [
    "vlsi","asic","fpga","rtl","verilog","systemverilog","uvm",
    "physical design","synthesis","sta","timing analysis",
    "floorplanning","place and route","eda","dft","low power design"
    ],

    "frontend_web": [
    "frontend","web ui","ui developer","spa","responsive design",
    "web interface","user interface","client side","ui ux"
    ],

    "backend_web": [
    "backend","server side","api development","rest api",
    "microservices","authentication","authorization",
    "scalable systems","backend engineer","distributed systems"
    ],

    "fullstack_web": [
    "full stack","fullstack","end to end web",
    "frontend and backend","full stack developer"
    ],

    "mobile_app": [
    "mobile application","android developer","ios developer",
    "mobile engineer","cross platform app","mobile ui"
    ],

    "ml_ai_dl_cv": [
    "machine learning","deep learning","artificial intelligence",
    "computer vision","nlp","predictive model","model training",
    "neural network","data driven model","ai engineer"
    ],

    "data_science": [
    "data science","statistical analysis","data modeling",
    "predictive analytics","exploratory data analysis",
    "hypothesis testing","applied statistics"
    ],

    "data_engineering": [
    "data engineering","etl","data pipeline","big data processing",
    "stream processing","batch processing","data warehouse",
    "lakehouse","data ingestion"
    ],

    "data_analytics": [
    "data analyst","dashboarding","reporting",
    "business intelligence","data visualization",
    "analytics reporting"
    ],

    "cloud": [
    "cloud engineer","cloud architecture","cloud deployment",
    "multi cloud","hybrid cloud","cloud migration",
    "serverless architecture"
    ],

    "devops": [
    "devops","ci cd","release pipeline","build pipeline",
    "infrastructure automation","site reliability",
    "platform engineering","monitoring and logging"
    ],

    "cyber_security": [
    "cyber security","information security","security analyst",
    "penetration testing","soc analyst","incident response",
    "threat detection","security monitoring"
    ],

    "ar_vr_xr": [
    "augmented reality","virtual reality","mixed reality",
    "xr developer","immersive application","spatial computing"
    ],

    "game_development": [
    "game developer","game engine developer","game programming",
    "real time graphics","gameplay programming"
    ],

    "iot": [
    "internet of things","connected devices","edge computing",
    "sensor network","device telemetry","embedded iot"
    ],

    "robotics": [
    "robotics engineer","robot software","autonomous systems",
    "robot perception","robot navigation","motion planning"
    ],

    "blockchain": [
    "blockchain developer","web3 developer",
    "decentralized application","smart contract development",
    "crypto application"
    ],

    "software_testing": [
    "software testing","quality assurance",
    "test automation engineer","manual tester",
    "test planning","test execution"
    ]
}

def normalize_text(text):
    text = text.lower()

    for k, v in abbr_map.items():
        text = text.replace(k, v)

    text = re.sub(r"[^a-z0-9\s]", " ", text)
    text = re.sub(r"\s+", " ", text).strip()

    return text

def generate_ngrams(words, n):
    result = []
    for i in range(len(words) - n + 1):
        phrase = " ".join(words[i:i+n])
        result.append(phrase)

    return result

def build_phrases(text):
    words = text.split()

    unigrams = words
    bigrams  = generate_ngrams(words, 2)
    trigrams = generate_ngrams(words, 3)

    return set(unigrams + bigrams + trigrams)

def detect_domains(job_description):

    text = normalize_text(job_description)
    phrases = build_phrases(text)

    scores = {}

    for domain, keys in domain_keywords.items():
        score = 0

        for k in keys:
            if k in phrases:
                score += 1

        scores[domain] = score

    return scores

def get_top_domain(scores):
    return max(scores, key=scores.get)

def jd(job_description):
    return job_description

def main():
    job_description=input("Enter detailed job description = ")
    score = detect_domains(job_description)
    top_domain = get_top_domain(score)
    return top_domain

if __name__=="__main__":
    main()