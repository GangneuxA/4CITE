import unittest
from app.routes import app ,db
from app.models import booking,user,chambres,hotel

class TestbookingGet(unittest.TestCase):
    def setUp(self):
        app.testing = True
        self.app_context = app.app_context()
        self.app_context.push()
        self.client = app.test_client()
        self.admin_token = self.create_admin_user(name="admin", mail="admin@example.com", role="admin")
        self.user_token = self.create_admin_user(name="user", mail="user@example.com", role="user")
        self.hotel_obj = hotel(name="Hotel ABC", location="City XYZ", description="A luxurious hotel")
        db.session.add(self.hotel_obj)
        db.session.commit()

        self.chambre1 = chambres(numero="101", nb_personne=2, hotel_id=self.hotel_obj.id)
        self.chambre2 = chambres(numero="102", nb_personne=2, hotel_id=self.hotel_obj.id)
        db.session.add_all([self.chambre1, self.chambre2])
        db.session.commit()

    def tearDown(self):
        admin_user = user.query.filter_by(email="admin@example.com").first()
        if admin_user:
            db.session.delete(admin_user)
            db.session.commit()

        user_user = user.query.filter_by(email="user@example.com").first()
        if user_user:
            db.session.delete(user_user)
            db.session.commit()
        db.session.delete(self.chambre1)
        db.session.delete(self.chambre2)
        db.session.delete(self.hotel_obj)
        db.session.commit()

    def test_get_booking_as_admin(self):
        with self.client:
            user1 = user.query.filter_by(email="user@example.com").first()
            user2 = user(pseudo="user",email="user2@example.com", role="user")
            user2.set_password('password')
            db.session.add(user2)
            db.session.commit()
            booking1 = booking(user_id=user1.id, chambre_id=self.chambre1.id, datein="2024-03-01", dateout="2024-03-05")
            booking2 = booking(user_id=user2.id, chambre_id=self.chambre2.id, datein="2024-03-10", dateout="2024-03-15")
            db.session.add_all([booking1, booking2])
            db.session.commit()
            response = self.client.get('/booking', headers={'Authorization': f'Bearer {self.admin_token}'})
            data = response.get_json()
            
            db.session.delete(booking1)
            db.session.delete(booking2)
            db.session.delete(user2)
            db.session.commit()

            self.assertEqual(response.status_code, 200)
            self.assertIsInstance(data, list)
            self.assertGreaterEqual(len(data), 2)

    def test_get_booking_for_specific_user_as_admin(self):
        with self.client:
            user1 = user.query.filter_by(email="user@example.com").first()
            booking1 = booking(user_id=user1.id, chambre_id=self.chambre1.id, datein="2024-03-01", dateout="2024-03-05")
            booking2 = booking(user_id=user1.id, chambre_id=self.chambre2.id, datein="2024-03-10", dateout="2024-03-15")
            db.session.add_all([booking1, booking2])
            db.session.commit()
            response = self.client.get(f'/booking?email={user1.email}', headers={'Authorization': f'Bearer {self.admin_token}'})
            data = response.get_json()
            
            db.session.delete(booking1)
            db.session.delete(booking2)
            db.session.commit()

            self.assertEqual(response.status_code, 200)
            self.assertIsInstance(data, list)
            self.assertEqual(len(data), 2)

    def test_get_booking_as_user(self):
        with self.client:
            user1 = user.query.filter_by(email="user@example.com").first()
            booking1 = booking(user_id=user1.id, chambre_id=self.chambre1.id, datein="2024-03-01", dateout="2024-03-05")
            booking2 = booking(user_id=user1.id, chambre_id=self.chambre2.id, datein="2024-03-10", dateout="2024-03-15")
            db.session.add_all([booking1, booking2])
            db.session.commit()
            response = self.client.get('/booking', headers={'Authorization': f'Bearer {self.user_token}'})
            data = response.get_json()

            db.session.delete(booking1)
            db.session.delete(booking2)
            db.session.commit()

            self.assertEqual(response.status_code, 200)
            self.assertIsInstance(data, list)
            self.assertEqual(len(data), 2)


    def create_admin_user(self, name , mail , role):
        admin_user = user(pseudo=name, email=mail, role=role)
        admin_user.set_password("admin_password")
        db.session.add(admin_user)
        db.session.commit()
        response = self.client.post('/login', json={'email': mail, 'password': 'admin_password'})
        data = response.get_json()
        return data['access_token']
    

class TestbookingPost(unittest.TestCase):
    def setUp(self):
        app.testing = True
        self.app_context = app.app_context()
        self.app_context.push()
        self.client = app.test_client()
        self.admin_token = self.create_admin_user(name="admin", mail="admin@example.com", role="admin")
        self.user_token = self.create_admin_user(name="user", mail="user@example.com", role="user")
        self.hotel_obj = hotel(name="Hotel ABC", location="City XYZ", description="A luxurious hotel")
        db.session.add(self.hotel_obj)
        db.session.commit()

        self.chambre1 = chambres(numero="101", nb_personne=2, hotel_id=self.hotel_obj.id)
        self.chambre2 = chambres(numero="102", nb_personne=2, hotel_id=self.hotel_obj.id)
        db.session.add_all([self.chambre1, self.chambre2])
        db.session.commit()

    def tearDown(self):
        admin_user = user.query.filter_by(email="admin@example.com").first()
        if admin_user:
            db.session.delete(admin_user)
            db.session.commit()

        user_user = user.query.filter_by(email="user@example.com").first()
        if user_user:
            db.session.delete(user_user)
            db.session.commit()
        db.session.delete(self.chambre1)
        db.session.delete(self.chambre2)
        db.session.delete(self.hotel_obj)
        db.session.commit()

    def test_create_booking_as_admin(self):
        with self.client:
            data = {
                'chambre_id': self.chambre1.id,
                'datein': '2024-03-01',
                'dateout': '2024-03-05'
            }
            response = self.client.post('/booking', json=data, headers={'Authorization': f'Bearer {self.admin_token}'})
            self.assertEqual(response.status_code, 201)
            created_booking = booking.query.filter_by(chambre_id=self.chambre1.id).first()
            self.assertIsNotNone(created_booking)

    def test_create_booking_as_user(self):
        with self.client:
            data = {
                'chambre_id': self.chambre1.id,
                'datein': '2024-03-01',
                'dateout': '2024-03-05'
            }

            response = self.client.post('/booking', json=data, headers={'Authorization': f'Bearer {self.user_token}'})
            user_user = user.query.filter_by(email="user@example.com").first()
            created_booking = booking.query.filter_by(chambre_id=self.chambre1.id, user_id=user_user.id).first()
            db.session.delete(created_booking)
            db.session.commit()

            self.assertEqual(response.status_code, 201)
            self.assertIsNotNone(created_booking)

    def test_create_booking_missing_parameters(self):
        with self.client:
            response = self.client.post('/booking', json={}, headers={'Authorization': f'Bearer {self.user_token}'})
            data = response.get_json()

            self.assertEqual(response.status_code, 400)
            self.assertIn('error', data)
            self.assertEqual(data['error'], 'json not found')

    def test_create_booking_unauthorized(self):
        with self.client:
            response = self.client.post('/booking', json={}, headers={'Authorization': 'Bearer invalidtoken'})
            self.assertEqual(response.status_code, 401)


    def create_admin_user(self, name , mail , role):
        admin_user = user(pseudo=name, email=mail, role=role)
        admin_user.set_password("admin_password")
        db.session.add(admin_user)
        db.session.commit()
        response = self.client.post('/login', json={'email': mail, 'password': 'admin_password'})
        data = response.get_json()
        return data['access_token']


if __name__ == '__main__':
    unittest.main()
    app.run()