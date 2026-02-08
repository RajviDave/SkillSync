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
    "embedded","microcontroller","firmware","rtos","bare metal",
    "arm cortex","stm32","arduino","raspberry pi","spi","i2c","uart"
    ],

    "vlsi": [
    "vlsi","asic","fpga","verilog","systemverilog","uvm","rtl",
    "physical design","synthesis","timing analysis","eda"
    ],

    "frontend_web": [
    "frontend","web ui","ui developer","HTML","CSS","javascript",
    "react","angular","vue","responsive","tailwind"
    ],

    "backend_web": [
    "backend","server side","api","rest api","microservices",
    "authentication","authorization","scalable systems"
    ],

    "fullstack_web": [
    "full stack","fullstack","end to end web","frontend and backend"
    ],

    "mobile_app": [
    "android","ios","mobile application","flutter","react native",
    "swift","kotlin","mobile developer"
    ],

    "ml_ai_dl_cv": [
    "machine learning","deep learning","artificial intelligence",
    "computer vision","nlp","model training","neural network",
    "pytorch","tensorflow","huggingface"
    ],

    "data_science": [
    "data science","statistical analysis","feature engineering",
    "exploratory data analysis","model evaluation"
    ],

    "data_engineering": [
    "data engineer","etl","pipeline","data pipeline","airflow",
    "spark","hadoop","kafka","big data","data warehouse"
    ],

    "data_analytics": [
    "data analyst","dashboard","reporting","power bi","tableau",
    "business intelligence","sql analysis"
    ],

    "cloud": [
    "cloud","aws","azure","gcp","cloud architecture",
    "serverless","cloud deployment"
    ],

    "devops": [
    "devops","ci cd","docker","kubernetes","jenkins",
    "monitoring","infrastructure as code","terraform"
    ],

    "cyber_security": [
    "security","cyber security","pentesting","vulnerability",
    "soc","network security","incident response","siem"
    ],

    "ar_vr_xr": [
    "augmented reality","virtual reality","mixed reality",
    "xr","unity","unreal","3d interaction","spatial computing"
    ],

    "game_development": [
    "game development","game engine","unity","unreal engine",
    "game programmer","3d game","c# game"
    ],

    "iot": [
    "iot","internet of things","sensor data","edge device",
    "mqtt","device integration"
    ],

    "robotics": [
    "robotics","ros","path planning","slam","robot control",
    "autonomous robot"
    ],

    "blockchain": [
    "blockchain","smart contract","web3","ethereum",
    "solidity","defi","dapp"
    ],

    "software_testing": [
    "qa","testing","automation testing","selenium",
    "test cases","manual testing"
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


def main():
    job_description=input("Enter detailed job description = ")
    score = detect_domains(job_description)
    top_domain = get_top_domain(score)
    return top_domain

if __name__=="__main__":
    main()