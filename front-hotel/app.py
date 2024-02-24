import datetime
from flask import Flask, flash, redirect, render_template, request, url_for
from wtforms import Form, BooleanField, StringField, PasswordField, validators

app = Flask(__name__)


@app.route('/home')
def home():
    return render_template('home.html', utc_dt=datetime.datetime.utcnow())

@app.route('/login')
def login():
    return render_template('login.html', utc_dt=datetime.datetime.utcnow())

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        email = request.form.get("email")
        print(email)
        return redirect(url_for('login'))
    return render_template('register.html')