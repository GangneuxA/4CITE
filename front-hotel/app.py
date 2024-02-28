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

def is_administration():
    try:
        role = session["role"]
        return role in ["admin", "employee"]
    except KeyError:
        return False

@app.route('/')
def base():
    return redirect(url_for('home'))

@app.route('/home', methods=['GET','POST'])
def home():
    if request.method == 'GET':

        administration = is_administration()
        authenticated = is_authenticated()

        url = URL + "hotel"

        response = requests.get(url=url, headers=HEADERS)
        hotels=response.json()

        images = []
        for hotel in hotels:

            url = URL + "image/" + str(hotel["id"])
            response = requests.get(url=url, headers=HEADERS)

            images.append(response.json())
        print(images)

        url = URL + "chambres"

        response = requests.get(url=url, headers=HEADERS)
        rooms=response.json()

        return render_template('home.html', authenticated=authenticated, administration=administration,hotels=hotels, images=images, rooms=rooms )
    
    if request.method == 'POST':

        room_id = request.form.get("room_id")

        return render_template('booking.html', room_id=room_id)

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
            session['access_token'] = response.json()["access_token"]
            session['email'] = response.json()["user"]["email"]
            session['role'] = response.json()["user"]["role"]
            session['pseudo'] = response.json()["user"]["pseudo"]
            session['id'] = response.json()["user"]["id"]
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
        session.clear()
        return redirect(url_for('home'))
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

@app.route('/user', methods=['GET'])
def user():
    if request.method == 'GET':
        administration = is_administration()
        authenticated = is_authenticated()
        if authenticated == True:
            url = URL + "user"

            HEADERS.update({"Authorization": "Bearer "+session['access_token']})

            response = requests.get(url=url, headers=HEADERS)

            if response.status_code == 200:
                print(response.json())
                return render_template('user.html', session=session, authenticated=authenticated, administration=administration )
            else: 
                return redirect(url_for('error'))
        else:
            return render_template('login.html')
    

@app.route('/change_user', methods=['GET', 'POST'])
def change_user():
    administration = is_administration()
    authenticated = is_authenticated()
    if request.method == 'GET':         
        return render_template('change_user.html',session=session, authenticated=authenticated, administration=administration)
    if request.method == 'POST':
        
        body = {}
        body.update({"pseudo": request.form.get("pseudo")})
        body.update({"email": request.form.get("email")})
        if request.form.get("password") != None:
            body.update({"password": request.form.get("password")})
        url = URL + "user/" + str(session["id"])

        HEADERS.update({"Authorization": "Bearer "+session['access_token']})

        response = requests.put(url=url, json=body, headers=HEADERS)

        session['email'] = request.form.get("email")
        session['pseudo'] = request.form.get("pseudo")

        return redirect(url_for('user'))
    
@app.route('/delete_user', methods=['POST'])
def delete_user():
    if request.method == 'POST':

        url = URL + "user"

        HEADERS.update({"Authorization": "Bearer "+session['access_token']})

        response = requests.delete(url=url, headers=HEADERS)
        session.clear()
        return redirect(url_for('home'))
    
@app.route('/administration', methods=['GET'])
def administration():
    if request.method == 'GET':
        authenticated = is_authenticated()
        administration = is_administration()
        url = URL + "user"

        HEADERS.update({"Authorization": "Bearer "+session['access_token']})

        response = requests.get(url=url, headers=HEADERS)

        if response.status_code == 200:
            print(response.json())
            return render_template('administration.html', session=session, authenticated=authenticated, administration=administration, users=response.json())
        else: 
            return redirect(url_for('error'))

@app.route('/booking', methods=['GET','POST'])
def booking():
    if request.method == 'POST':

        url = URL + "booking"

        body = {}
        body.update({"chambre_id":request.form.get("room_id")})
        body.update({"user_id":session['id']})
        body.update({"datein":request.form.get("datein")})
        body.update({"dateout":request.form.get("dateout")})

        HEADERS.update({"Authorization": "Bearer "+session['access_token']})

        response = requests.post(url=url, json=body, headers=HEADERS)

        return redirect(url_for('booking'))

    if request.method == 'GET':
        administration = is_administration()
        authenticated = is_authenticated()
        if authenticated == True:
            url = URL + "booking"

            HEADERS.update({"Authorization": "Bearer "+session['access_token']})

            response = requests.get(url=url, headers=HEADERS)

            if response.status_code == 200:
                print(response.json())
                return render_template('reservations.html', reservations=response.json(), authenticated=authenticated, administration=administration )
            else: 
                return redirect(url_for('error'))
        else:
            return render_template('login.html')
    
@app.route('/change_booking', methods=['GET', 'POST'])
def change_booking():
    administration = is_administration()
    authenticated = is_authenticated()
    if request.method == 'GET':     

        reservation = json.loads(request.args.get("booking").replace("\'", "\"")) 
        
        return render_template('change_booking.html',reservation=reservation, authenticated=authenticated, administration=administration)
    if request.method == 'POST':

        body = {}
        if request.form.get("datein") != "":
            body.update({"datein": request.form.get("datein")})
        if request.form.get("dateout") != "":
            body.update({"dateout": request.form.get("dateout")})
        
        url = URL + "booking/" + request.form.get("booking_id")

        print(request.form.get("booking_id"))

        HEADERS.update({"Authorization": "Bearer "+session['access_token']})

        response = requests.put(url=url, json=body, headers=HEADERS)
        print("######")
        return redirect(url_for('booking'))
    
@app.route('/delete_booking', methods=['POST'])
def delete_booking():
    if request.method == 'POST':

        url = URL + "booking/" + request.form.get("booking_id")

        HEADERS.update({"Authorization": "Bearer "+session['access_token']})

        response = requests.delete(url=url, headers=HEADERS)

        return redirect(url_for('booking'))