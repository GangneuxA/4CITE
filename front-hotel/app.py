import datetime
import json
from flask import Flask, flash, redirect, render_template, request, url_for, session
from wtforms import Form, BooleanField, StringField, PasswordField, validators
import requests
import os

app = Flask(__name__)

app.secret_key = os.urandom(24)

URL = "http://localhost:5000/"
HEADERS = {"accept":"*/*",
           "Content-Type": "application/json"}

def is_authenticated():
    return session.get('authenticated', False)

@app.route('/home')
def home():
    authenticated = is_authenticated()
    return render_template('home.html', authenticated=authenticated)

@app.route('/error')
def error():
    return render_template('error.html', utc_dt=datetime.datetime.utcnow())

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':

        url = URL + "login"
        body = {"email": request.form.get("email"),
                "password": request.form.get("password")}
        
        response = requests.post(url=url, json=body, headers=HEADERS)

        if response.status_code == 200:
            access_token = response.json()["access_token"]
            session['access_token'] = access_token
            session['authenticated'] = True
            return redirect(url_for('home'))
        else: 
            return redirect(url_for('error'))
    return render_template('login.html', utc_dt=datetime.datetime.utcnow())

@app.route('/logout', methods=['POST'])
def logout():
    url = URL + "logout"
    HEADERS.update({"Authorization": "Bearer "+session['access_token']})

    response = requests.post(url=url, headers=HEADERS)

    if response.status_code == 200:
        session.pop('authenticated', None)
        session['access_token'] = None
        return render_template('home.html', utc_dt=datetime.datetime.utcnow())
    else: 
        return redirect(url_for('error'))

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':

        url = URL + "user"
        body = {"pseudo": request.form.get("pseudo"),
                "email": request.form.get("email"),
                "password": request.form.get("password")}
        
        response = requests.post(url=url, json=body, headers=HEADERS)

        if response.status_code == 201:
            return redirect(url_for('login'))
        else: 
            return redirect(url_for('error'))
    return render_template('register.html')

@app.route('/user', methods=['GET', 'PUT', 'DELETE'])
def user():
    if request.method == 'GET':

        url = URL + "user"

        HEADERS.update({"Authorization": "Bearer "+session['access_token']})

        response = requests.get(url=url, headers=HEADERS)

        if response.status_code == 200:
            print(response.json())
            authenticated = is_authenticated()
            return render_template('user.html', result=response.json(), authenticated=authenticated )
        else: 
            return redirect(url_for('error'))
         
    return render_template('home.html')