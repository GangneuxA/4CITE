from . import db

class hotel(db.Model):
    __tablename__ = 'hotel'
    id = db.Column(db.Integer, primary_key=True,autoincrement=True)
    name = db.Column(db.String(255), nullable=False)
    location = db.Column(db.String(255), nullable=False)
    description = db.Column(db.String(255), nullable=False)
    # description = db.Column(db.Float)
    

    def to_json(self):
        return {
            'id': self.id,
            'name': self.name,
            'location': self.location,
            'description': self.description
        }