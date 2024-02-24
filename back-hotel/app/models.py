from . import db
from werkzeug.security import generate_password_hash, check_password_hash
import base64


class hotel(db.Model):
    __tablename__ = 'hotel'
    id = db.Column(db.Integer, primary_key=True,autoincrement=True)
    name = db.Column(db.String(255), nullable=False)
    location = db.Column(db.String(255), nullable=False)
    description = db.Column(db.String(255), nullable=False)
    create_at = db.Column(db.DateTime(timezone=True), default=db.func.now())
    
    def to_json(self):
        return {
            'id': self.id,
            'name': self.name,
            'location': self.location,
            'description': self.description,
            'create_at': self.create_at
        }

class Image(db.Model):
    id = db.Column(db.Integer, primary_key=True,autoincrement=True)
    name = db.Column(db.String(100))
    data = db.Column(db.LargeBinary)
    hotel_id = db.Column(db.Integer, db.ForeignKey('hotel.id'), nullable=False)
    
    def to_json(self):
        return {
            'id': self.id,
            'name': self.name,
            'data': base64.b64encode(self.data).decode('utf-8'),
            'hotel_id': self.hotel_id,
        }
    

class chambres(db.Model):
    __tablename__ = 'chambres'
    id = db.Column(db.Integer, primary_key=True,autoincrement=True)
    numero = db.Column(db.String(20), nullable=False)
    nb_personne = db.Column(db.Integer, nullable=False)
    hotel_id = db.Column(db.Integer, db.ForeignKey('hotel.id'), nullable=False)
    
    def to_json(self):
        return {
            'id': self.id,
            'numero': self.numero,
            'nb_personne': self.nb_personne,
            'hotel_id': self.hotel_id
        }
    

class user(db.Model):
    __tablename__ = 'user'
    id = db.Column(db.Integer, primary_key=True,autoincrement=True)
    pseudo = db.Column(db.String(30), nullable=False)
    email = db.Column(db.String(30), nullable=False, unique=True)
    role = db.Column(db.String(30), nullable=False, default="user")
    password= db.Column(db.String(256), nullable=False)

    def set_password(self, password):
        self.password = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password, password)

    
    def to_json(self):
        return {
            'id': self.id,
            'pseudo': self.pseudo,
            'email': self.email,
            'role': self.role
        } 
    
class booking(db.Model):
    __tablename__ = 'booking'
    id = db.Column(db.Integer, primary_key=True,autoincrement=True)
    chambre_id = db.Column(db.Integer, db.ForeignKey('chambres.id'), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    datein = db.Column(db.Date, nullable=False)
    dateout = db.Column(db.Date, nullable=False)

    def to_json(self):
        return {
            'id': self.id,
            'chambre_id': self.chambre_id,
            'user_id': self.user_id,
            'datein': self.datein,
            'dateout': self.dateout
        } 