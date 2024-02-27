import unittest
from app.routes import app ,db
from app.models import booking,user,chambres,hotel,Image
import io
from PIL import Image as PILImage

class Testintegration(unittest.TestCase):
    def setUp(self):
        app.testing = True
        self.app_context = app.app_context()
        self.app_context.push()
        self.app = app.test_client()
        self.hotel_obj = hotel(name="Hotel ABC", location="City XYZ", description="A luxurious hotel")
        db.session.add(self.hotel_obj)
        db.session.commit()

        self.chambre1 = chambres(numero="101", nb_personne=2, hotel_id=self.hotel_obj.id)
        self.chambre2 = chambres(numero="102", nb_personne=2, hotel_id=self.hotel_obj.id)
        db.session.add_all([self.chambre1, self.chambre2])
        db.session.commit()

    def tearDown(self):
        db.session.delete(self.chambre1)
        db.session.delete(self.chambre2)
        db.session.delete(self.hotel_obj)
        db.session.commit()

    def test_register_login_and_book_integration(self):
        user_data = {'pseudo': 'test_user', 'email': 'test2@example.com', 'password': 'password'}
        response = self.app.post('/user', json=user_data)
        self.assertEqual(response.status_code, 201)

        login_data = {'email': 'test2@example.com', 'password': 'password'}
        response = self.app.post('/login', json=login_data)
        self.assertEqual(response.status_code, 200)
        access_token = response.json['access_token']

        response = self.app.get('/hotel', headers={'Authorization': f'Bearer {access_token}'})
        self.assertEqual(response.status_code, 200)
        hotel_id = response.json[0]['id']

        response = self.app.get(f'/chambres?hotel_id={hotel_id}')
        self.assertEqual(response.status_code, 200)
        chambres_obj = response.json
        self.assertTrue(isinstance(chambres_obj, list))
        self.assertTrue(len(chambres_obj) > 0)

        reservation_data = {'chambre_id': chambres_obj[0]['id'], 'datein': '2024-03-01', 'dateout': '2024-03-05'}
        response = self.app.post('/booking', json=reservation_data, headers={'Authorization': f'Bearer {access_token}'})
        self.assertEqual(response.status_code, 201)

        response = self.app.get('/booking', headers={'Authorization': f'Bearer {access_token}'})
        self.assertEqual(response.status_code, 200)

        self.assertEqual(response.json[0]["user_id"], user.query.filter_by(email='test2@example.com').first().id)
        self.assertEqual(response.json[0]["chambre_id"], chambres_obj[0]['id'])


        booking_objet = booking.query.filter_by(id=response.json[0]["id"]).first()
        db.session.delete(booking_objet)
        user_objet = user.query.filter_by(email='test2@example.com').first()
        db.session.delete(user_objet)
        db.session.commit()

    def test_register_and_promote_to_admin_integration(self):
        user_data = {'pseudo': 'test_user', 'email': 'test@example.com', 'password': 'password'}
        response = self.app.post('/user', json=user_data)
        self.assertEqual(response.status_code, 201)

        user_obj= user.query.filter_by(email='test@example.com').first()
        user_obj.role= "admin"
        db.session.commit()

        admin_login_data = {'email': 'test@example.com', 'password': 'password'}
        admin_response = self.app.post('/login', json=admin_login_data)
        self.assertEqual(admin_response.status_code, 200)
        admin_access_token = admin_response.json['access_token']


        hotel_data = {'name': 'Hotel Test', 'location': 'City A', 'description': 'Test Hotel Description'}
        hotel_response = self.app.post('/hotel', json=hotel_data, headers={'Authorization': f'Bearer {admin_access_token}'})
        self.assertEqual(hotel_response.status_code, 201)
        hotel_id = hotel_response.json['id']

        chambre_data = {'numero': '101', 'nb_personne': 2, 'hotel_id': hotel_id}
        chambre_response = self.app.post('/chambres', json=chambre_data, headers={'Authorization': f'Bearer {admin_access_token}'})
        self.assertEqual(chambre_response.status_code, 201)
        chambre_id = chambre_response.json['id']

        fake_image_data = PILImage.new('RGB', (100, 100)).tobytes()
        fake_image = io.BytesIO(fake_image_data)
        fake_image.name = 'test_image.jpg'
        image_data = {'image': (fake_image, 'test_image.jpg'), 'hotel_id': hotel_id }
        image_response = self.app.post('/image', data=image_data, headers={'Authorization': f'Bearer {admin_access_token}'})
        self.assertEqual(image_response.status_code, 200)

        image_response = Image.query.filter_by(hotel_id=hotel_id).first()
        self.assertIsNotNone(image_response)

        chambres_response = chambres.query.filter_by(id=chambre_id).first()
        self.assertIsNotNone(chambres_response)

        hotel_response = hotel.query.filter_by(id=hotel_id).first()
        self.assertIsNotNone(hotel_response)

        user_reponse = user.query.filter_by(email='test@example.com').first()

        db.session.delete(image_response)
        db.session.delete(chambres_response)
        db.session.delete(hotel_response)
        db.session.delete(user_reponse)
        db.session.commit()

    def test_register_and_promote_to_employee_integration(self):
        user_data = {'pseudo': 'test_user', 'email': 'employee@example.com', 'password': 'password'}
        response = self.app.post('/user', json=user_data)
        self.assertEqual(response.status_code, 201)
        user_data = {'pseudo': 'test_user', 'email': 'user3@example.com', 'password': 'password'}
        response = self.app.post('/user', json=user_data)
        self.assertEqual(response.status_code, 201)

        user_obj= user.query.filter_by(email='employee@example.com').first()
        user_obj.role= "employee"
        db.session.commit()

        admin_login_data = {'email': 'employee@example.com', 'password': 'password'}
        admin_response = self.app.post('/login', json=admin_login_data)
        self.assertEqual(admin_response.status_code, 200)
        admin_access_token = admin_response.json['access_token']

        user_response = self.app.get('/user', headers={'Authorization': f'Bearer {admin_access_token}'})
        self.assertEqual(user_response.status_code, 200)
        self.assertTrue(isinstance(user_response.json, list))

        employee_reponse = user.query.filter_by(email='employee@example.com').first()
        user_reponse = user.query.filter_by(email='user3@example.com').first()

        db.session.delete(employee_reponse)
        db.session.delete(user_reponse)
        db.session.commit()
if __name__ == '__main__':
    unittest.main()
    app.run()