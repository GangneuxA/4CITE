import datetime
from flask import Flask, render_template

app = Flask(__name__)


@app.route('/home')
def home():
    return render_template('home.html', utc_dt=datetime.datetime.utcnow())

@app.route('/login')
def login():
    return render_template('login.html', utc_dt=datetime.datetime.utcnow())

@app.route('/register')
def register():
    return render_template('register.html', utc_dt=datetime.datetime.utcnow())