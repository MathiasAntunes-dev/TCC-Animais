import os
from dotenv import load_dotenv
from flask import Flask, render_template
from models.database import init_db

load_dotenv()

app = Flask(__name__)
app.secret_key = os.getenv("SECRET_KEY", "chave_padrao_para_testes")

UPLOAD_FOLDER = 'static/uploads'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

init_db()

@app.route("/")
def home():
    return render_template('home.html')

@app.route("/faq")
def faq():
    return render_template('faq.html')

@app.route("/sobreProjeto")
def sobreProjeto():
    return render_template('sobreProjeto.html')

@app.route("/login")
def login():
    return render_template('login.html')

