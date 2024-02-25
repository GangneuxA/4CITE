import unittest
from app.routes import app ,db
from app.models import hotel,user

class TestHotelGet(unittest.TestCase):
    def setUp(self):
        app.testing = True
        self.app_context = app.app_context()
        self.app_context.push()
        self.client = app.test_client()

    def test_get_hotels_default_limit(self):
        with self.client:
            for i in range(15):
                db.session.add(hotel(name=f"Hotel {i}", location=f"Location {i}", description=f"description {i}" ))
            db.session.commit()
                
            response = self.client.get('/hotel')
            data = response.get_json()

            for i in range(15):
                db.session.delete(hotel.query.filter_by(name=f"Hotel {i}").first())
            db.session.commit()
            
            self.assertEqual(response.status_code, 200)
            self.assertEqual(len(data), 10)

    def test_get_hotels_custom_limit(self):
        with self.client:
            # Créer quelques hôtels pour tester
            for i in range(15):
                db.session.add(hotel(name=f"Hotel {i}", location=f"Location {i}", description=f"description {i}"))
            db.session.commit()

            # Effectuer la requête GET pour obtenir les hôtels avec une limite personnalisée
            custom_limit = 5
            response = self.client.get(f'/hotel?limit={custom_limit}')
            data = response.get_json()

            for i in range(15):
                db.session.delete(hotel.query.filter_by(name=f"Hotel {i}").first())
            db.session.commit()

            self.assertEqual(response.status_code, 200)
            self.assertEqual(len(data), custom_limit)


class TestHotelPost(unittest.TestCase):
    def setUp(self):
        app.testing = True
        self.app_context = app.app_context()
        self.app_context.push()
        self.client = app.test_client()
        self.admin_token = self.create_admin_user(name="admin", mail="admin@example.com", role="admin")
        self.user_token = self.create_admin_user(name="user", mail="user@example.com", role="user")

    def tearDown(self):
        admin_user = user.query.filter_by(email="admin@example.com").first()
        if admin_user:
            db.session.delete(admin_user)
            db.session.commit()

        user_user = user.query.filter_by(email="user@example.com").first()
        if user_user:
            db.session.delete(user_user)
            db.session.commit()

    def test_create_hotel_as_admin(self):
        with self.client:
            hotel_data = {
                'name': 'Hotel ABC',
                'location': 'City XYZ',
                'description': 'A luxurious hotel in the heart of the city'
            }
            response = self.client.post('/hotel', json=hotel_data, headers={'Authorization': f'Bearer {self.admin_token}'})
            created_hotel = hotel.query.filter_by(name=hotel_data['name']).first()
            db.session.delete(created_hotel)
            db.session.commit()

            self.assertEqual(response.status_code, 201)
            self.assertIsNotNone(created_hotel)
            self.assertEqual(created_hotel.location, hotel_data['location'])
            self.assertEqual(created_hotel.description, hotel_data['description'])

    def test_create_hotel_missing_parameters(self):
        with self.client:
            hotel_data = {
                'name': 'Hotel ABC',
                'location': 'City XYZ'
            }
            response = self.client.post('/hotel', json=hotel_data, headers={'Authorization': f'Bearer {self.admin_token}'})
            data = response.get_json()

            self.assertEqual(response.status_code, 400)
            self.assertIn('error', data)
            self.assertEqual(data['error'], 'missing parameter')

    def test_create_hotel_unauthorized(self):
        with self.client:
            hotel_data = {
                'name': 'Hotel ABC',
                'location': 'City XYZ',
                'description': 'A luxurious hotel in the heart of the city'
            }
            response = self.client.post('/hotel', json=hotel_data, headers={'Authorization': f'Bearer {self.user_token}'})
            data = response.get_json()

            self.assertEqual(response.status_code, 404)
            self.assertIn('error', data)
            self.assertEqual(data['error'], 'You have not the permission for this')

    def create_admin_user(self, name , mail , role):
        admin_user = user(pseudo=name, email=mail, role=role)
        admin_user.set_password("admin_password")
        db.session.add(admin_user)
        db.session.commit()
        response = self.client.post('/login', json={'email': mail, 'password': 'admin_password'})
        data = response.get_json()
        return data['access_token']
    
class TestHotelPut(unittest.TestCase):
    def setUp(self):
        app.testing = True
        self.app_context = app.app_context()
        self.app_context.push()
        self.client = app.test_client()
        self.admin_token = self.create_admin_user(name="admin", mail="admin@example.com", role="admin")
        self.user_token = self.create_admin_user(name="user", mail="user@example.com", role="user")

    def tearDown(self):
        admin_user = user.query.filter_by(email="admin@example.com").first()
        if admin_user:
            db.session.delete(admin_user)
            db.session.commit()

        user_user = user.query.filter_by(email="user@example.com").first()
        if user_user:
            db.session.delete(user_user)
            db.session.commit()

    def test_update_hotel_as_admin(self):
        with self.client:
            hotel_obj = hotel(name="Hotel ABC", location="City XYZ", description="A luxurious hotel")
            db.session.add(hotel_obj)
            db.session.commit()

            updated_data = {
                'name': 'Updated Hotel Name',
                'location': 'Updated City Name',
                'description': 'Updated description'
            }
            response = self.client.put(f'/hotel/{hotel_obj.id}', json=updated_data, headers={'Authorization': f'Bearer {self.admin_token}'})
            updated_hotel = hotel.query.get(hotel_obj.id)
            db.session.delete(updated_hotel)
            db.session.commit()

            self.assertEqual(response.status_code, 200)
            self.assertEqual(updated_hotel.name, updated_data['name'])
            self.assertEqual(updated_hotel.location, updated_data['location'])
            self.assertEqual(updated_hotel.description, updated_data['description'])

    def test_update_hotel_unauthorized(self):
        with self.client:
            hotel_obj = hotel(name="Hotel ABC", location="City XYZ", description="A luxurious hotel")
            db.session.add(hotel_obj)
            db.session.commit()

            updated_data = {
                'name': 'Updated Hotel Name',
                'location': 'Updated City Name',
                'description': 'Updated description'
            }
            response = self.client.put(f'/hotel/{hotel_obj.id}', json=updated_data, headers={'Authorization': f'Bearer {self.user_token}'})
            data = response.get_json()
            db.session.delete(hotel_obj)
            db.session.commit()
            
            self.assertEqual(response.status_code, 404)
            self.assertIn('error', data)
            self.assertEqual(data['error'], 'You have not the permission for this')

    def test_update_hotel_not_found(self):
        with self.client:
            nonexistent_hotel_id = 9999
            updated_data = {
                'name': 'Updated Hotel Name',
                'location': 'Updated City Name',
                'description': 'Updated description'
            }
            response = self.client.put(f'/hotel/{nonexistent_hotel_id}', json=updated_data, headers={'Authorization': f'Bearer {self.admin_token}'})
            self.assertEqual(response.status_code, 404)
            data = response.get_json()
            self.assertIn('error', data)
            self.assertEqual(data['error'], 'hotel not found')

    def create_admin_user(self, name , mail , role):
        admin_user = user(pseudo=name, email=mail, role=role)
        admin_user.set_password("admin_password")
        db.session.add(admin_user)
        db.session.commit()
        response = self.client.post('/login', json={'email': mail, 'password': 'admin_password'})
        data = response.get_json()
        return data['access_token']
    
class TestHotelDelete(unittest.TestCase):
    def setUp(self):
        app.testing = True
        self.app_context = app.app_context()
        self.app_context.push()
        self.client = app.test_client()
        self.admin_token = self.create_admin_user(name="admin", mail="admin@example.com", role="admin")
        self.user_token = self.create_admin_user(name="user", mail="user@example.com", role="user")

    def tearDown(self):
        admin_user = user.query.filter_by(email="admin@example.com").first()
        if admin_user:
            db.session.delete(admin_user)
            db.session.commit()

        user_user = user.query.filter_by(email="user@example.com").first()
        if user_user:
            db.session.delete(user_user)
            db.session.commit()

    def test_delete_hotel_as_admin(self):
        with self.client:
            hotel_obj = hotel(name="Hotel ABC", location="City XYZ", description="A luxurious hotel")
            db.session.add(hotel_obj)
            db.session.commit()

            response = self.client.delete(f'/hotel/{hotel_obj.id}', headers={'Authorization': f'Bearer {self.admin_token}'})
            deleted_hotel = hotel.query.get(hotel_obj.id)

            self.assertEqual(response.status_code, 200)
            self.assertIsNone(deleted_hotel)

    def test_delete_hotel_unauthorized(self):
        with self.client:
            hotel_obj = hotel(name="Hotel ABC", location="City XYZ", description="A luxurious hotel")
            db.session.add(hotel_obj)
            db.session.commit()

            response = self.client.delete(f'/hotel/{hotel_obj.id}', headers={'Authorization': f'Bearer {self.user_token}'})
            data = response.get_json()
            db.session.delete(hotel_obj)
            db.session.commit()

            self.assertEqual(response.status_code, 404)
            self.assertIn('error', data)
            self.assertEqual(data['error'], 'You have not the permission for this')

    def test_delete_hotel_not_found(self):
        with self.client:
            nonexistent_hotel_id = 9999
            response = self.client.delete(f'/hotel/{nonexistent_hotel_id}', headers={'Authorization': f'Bearer {self.admin_token}'})
            data = response.get_json()

            self.assertEqual(response.status_code, 404)
            self.assertIn('error', data)
            self.assertEqual(data['error'], 'hotel not found')

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