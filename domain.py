import nltk
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize


job_description=input("Enter Job description = ")

stop_words=set(stopwords.words('english'))
tokens=word_tokenize(job_description.lower())

filtered_tokens = [word for word in tokens if word not in stop_words]


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
    "frontend","web ui","ui developer","html","css","javascript",
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
