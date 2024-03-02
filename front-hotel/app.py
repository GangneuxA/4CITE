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

@app.route('/')
def base():
    return redirect(url_for('home'))

@app.route('/home', methods=['GET','POST'])
def home():
    if request.method == 'GET':

        url = URL + "hotel"

        response = requests.get(url=url, headers=HEADERS)
        hotels=response.json()

        for hotel in hotels:

            url = URL + "image/" + str(hotel["id"])
            response = requests.get(url=url, headers=HEADERS)

            hotel["image"] = response.json()

        url = URL + "chambres"

        response = requests.get(url=url, headers=HEADERS)
        rooms=response.json()

        return render_template('home.html', hotels=hotels, rooms=rooms )
    
    if request.method == 'POST':
        try:
            if session['authenticated']:
                room_id = request.form.get("room_id")

                return render_template('booking.html', room_id=room_id)
        except:
            return redirect(url_for('login'))

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
        try:
            if session['authenticated']:
                url = URL + "user"

                HEADERS.update({"Authorization": "Bearer "+session['access_token']})

                response = requests.get(url=url, headers=HEADERS)

                if response.status_code == 200:
                    print(response.json())
                    return render_template('user.html')
                else: 
                    return redirect(url_for('error'))
        except:
            return render_template('login.html')
    

@app.route('/change_user', methods=['GET', 'POST'])
def change_user():

    if request.method == 'GET':         
        return render_template('change_user.html')
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

        url = URL + "user"

        HEADERS.update({"Authorization": "Bearer "+session['access_token']})

        response = requests.get(url=url, headers=HEADERS)

        if response.status_code == 200:
            print(response.json())
            return render_template('administration.html', users=response.json())
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
        try:
            if session['authenticated'] == True:
                url = URL + "booking"

                HEADERS.update({"Authorization": "Bearer "+session['access_token']})

                response = requests.get(url=url, headers=HEADERS)

                if response.status_code == 200:
                    print(response.json())
                    return render_template('reservations.html', reservations=response.json())
                else: 
                    return redirect(url_for('error'))
        except:
            return render_template('login.html')
    
@app.route('/change_booking', methods=['GET', 'POST'])
def change_booking():

    if request.method == 'GET':     

        reservation = json.loads(request.args.get("booking").replace("\'", "\"")) 
        
        return render_template('change_booking.html',reservation=reservation)
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

        if session['role'] == 'admin':
             return redirect(url_for('admin_bookings'))
        return redirect(url_for('booking'))
    
@app.route('/delete_booking', methods=['POST'])
def delete_booking():
    if request.method == 'POST':

        url = URL + "booking/" + request.form.get("booking_id")

        HEADERS.update({"Authorization": "Bearer "+session['access_token']})

        response = requests.delete(url=url, headers=HEADERS)

        if session['role'] == "admin":
             return redirect(url_for('admin_bookings'))
        return redirect(url_for('booking'))
    
@app.route('/admin_hotels', methods=['GET','POST'])
def admin_hotels():
    if request.method == 'GET':

        url = URL + "hotel"

        response = requests.get(url=url, headers=HEADERS)
        hotels=response.json()

        return render_template('Admin_hotels.html', hotels=hotels)
    
@app.route('/hotel', methods=['GET','POST'])
def hotel():
    if request.method == 'GET':
        return render_template('hotel.html')
    if request.method == 'POST':
        
        url = URL + "hotel"

        HEADERS.update({"Authorization": "Bearer "+session['access_token']})

        body = {"name": request.form.get("name"),
                "description": request.form.get("description"),
                "location": request.form.get("location")}
        
        response = requests.post(url=url, json=body, headers=HEADERS)

        if response.status_code == 201:
            return redirect(url_for('admin_hotels'))
        else: 
            return redirect(url_for('error'))
 
    
@app.route('/change_hotel', methods=['GET','POST'])
def change_hotel():
    if request.method == 'GET':
        return render_template('change_hotel.html', hotel_id=request.args.get("hotel_id"))
    if request.method == 'POST':

        url = URL + "hotel/" + request.form.get("hotel_id")
        
        HEADERS.update({"Authorization": "Bearer "+session['access_token']})

        body = {}
        if request.form.get("name") != "":
            body.update({"name": request.form.get("name")})
        if request.form.get("description") != "":
            body.update({"description": request.form.get("description")})
        if request.form.get("location") != "":
            body.update({"location": request.form.get("location")})

        response = requests.put(url=url,json=body, headers=HEADERS)

        return redirect(url_for('admin_hotels'))
    
@app.route('/delete_hotel', methods=['POST'])
def delete_hotel():
    if request.method == 'POST':

        url = URL + "hotel/" + request.form.get("hotel_id")

        HEADERS.update({"Authorization": "Bearer "+session['access_token']})

        response = requests.delete(url=url, headers=HEADERS)

        return redirect(url_for('admin_hotels'))
    

@app.route('/admin_bookings', methods=['GET'])
def admin_bookings():
    if request.method == 'GET':

        url = URL + "booking"

        HEADERS.update({"Authorization": "Bearer "+session['access_token']})

        response = requests.get(url=url, headers=HEADERS)
        reservations=response.json()

        return render_template('Admin_bookings.html', reservations=reservations)
    
@app.route('/images', methods=['GET','POST'])
def images():
    if request.method == 'GET':

        url = URL + "hotel"

        response = requests.get(url=url, headers=HEADERS)
        hotels=response.json()

        for hotel in hotels:

            url = URL + "image/" + str(hotel["id"])
            response = requests.get(url=url, headers=HEADERS)

            hotel["image"] = response.json()

        return render_template('images.html', hotels=hotels)
    
    if request.method == 'POST':
        url = URL + "image" 

        body = {}
        file = request.files['image']
        image_name = file.filename  
        files = {'image': (image_name, file.read())}
        body.update({"hotel_id":request.form.get("hotel_id")})
        
        headers = {}
        headers.update({"Authorization": "Bearer "+session['access_token']})
        headers.update({"accept": "*/*"})
        
        print(url)
        print(headers)
        
        response = requests.post(url=url, data=body, files=files, headers=headers)
        
        return redirect(url_for('images'))
    
@app.route('/delete_image', methods=['POST'])
def delete_image():
    if request.method == 'POST':

        url = URL + "image/" + request.form.get("hotel_id") + "/" + request.form.get("image_id")

        HEADERS.update({"Authorization": "Bearer "+session['access_token']})

        response = requests.delete(url=url, headers=HEADERS)

        return redirect(url_for('images'))
    
@app.route('/rooms', methods=['GET','POST'])
def rooms():
    if request.method == 'GET':

        url = URL + "chambres"

        response = requests.get(url=url, headers=HEADERS)
        rooms=response.json()

        url = URL + "hotel"

        response = requests.get(url=url, headers=HEADERS)
        hotels=response.json()

        return render_template('Admin_rooms.html', rooms=rooms, hotels=hotels)
    
    if request.method == 'POST':

        url = URL + "chambres"

        HEADERS.update({"Authorization": "Bearer "+session['access_token']})

        body = {"numero": request.form.get("numero"),
                "nb_personne": request.form.get("nb_personne"),
                "hotel_id": request.form.get("hotel_id")}
        
        response = requests.post(url=url, json=body, headers=HEADERS)

        if response.status_code == 201:
            return redirect(url_for('rooms'))
        else: 
            return redirect(url_for('error'))

@app.route('/change_room', methods=['GET','POST'])
def change_room():
    if request.method == 'GET':
        return render_template('change_room.html', room_id=request.args.get("room_id"))
    if request.method == 'POST':

        url = URL + "chambres/" + request.form.get("room_id")
        
        HEADERS.update({"Authorization": "Bearer "+session['access_token']})

        body = {}
        if request.form.get("number") != "":
            body.update({"number": str(request.form.get("number"))})
        if request.form.get("nb_personne") != "":
            body.update({"nb_personne": int(request.form.get("nb_personne"))})

        print(body)
        response = requests.put(url=url, json=body, headers=HEADERS)

        return redirect(url_for('rooms'))
    
@app.route('/delete_room', methods=['POST'])
def delete_room():
    if request.method == 'POST':

        url = URL + "chambres/" + request.form.get("room_id")

        HEADERS.update({"Authorization": "Bearer "+session['access_token']})

        response = requests.delete(url=url, headers=HEADERS)

        return redirect(url_for('rooms'))

@app.route('/create_room', methods=['GET'])
def create_room():
    if request.method == 'GET':
        hotel_id = request.args.get("hotel_id")
        return render_template('room.html', hotel_id=hotel_id)