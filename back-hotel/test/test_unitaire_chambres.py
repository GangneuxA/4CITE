import unittest
from app.routes import app ,db
from app.models import chambres, user , hotel

class TestChambresGet(unittest.TestCase):
    def setUp(self):
        app.testing = True
        self.app_context = app.app_context()
        self.app_context.push()
        self.client = app.test_client()

    def test_get_chambres_no_query_params(self):
        with self.client:
            hotel_obj = hotel(name="Hotel ABC", location="City XYZ", description="A luxurious hotel")
            db.session.add(hotel_obj)
            db.session.commit()

            chambre1 = chambres(numero="101", nb_personne=2, hotel_id=hotel_obj.id)
            chambre2 = chambres(numero="102", nb_personne=2, hotel_id=hotel_obj.id)
            chambre3 = chambres(numero="103", nb_personne=3, hotel_id=hotel_obj.id)
            chambre4 = chambres(numero="104", nb_personne=3, hotel_id=hotel_obj.id)
            chambre5 = chambres(numero="105", nb_personne=4, hotel_id=hotel_obj.id)
            db.session.add_all([chambre1, chambre2, chambre3, chambre4, chambre5])
            db.session.commit()

            response = self.client.get('/chambres?hotel_id='+str(hotel_obj.id))
            data = response.get_json()
            for i in [chambre1, chambre2, chambre3, chambre4, chambre5,hotel_obj]:
                db.session.delete(i)
            db.session.commit()

            self.assertEqual(response.status_code, 200)
            self.assertIsInstance(data, list)
            self.assertEqual(len(data), 5)

    def test_get_chambres_with_limit_query_param(self):
        with self.client:
            hotel_obj = hotel(name="Hotel ABC", location="City XYZ", description="A luxurious hotel")
            db.session.add(hotel_obj)
            db.session.commit()

            listchambre=[]
            for i in range(15):
                chambre = chambres(numero=f"Chambre {i}", nb_personne=2, hotel_id=hotel_obj.id)
                listchambre.append(chambre)
                db.session.add(chambre)
            db.session.commit()

            response = self.client.get('/chambres?limit=15')
            data = response.get_json()

            for i in listchambre:
                db.session.delete(i)
            db.session.delete(hotel_obj)
            db.session.commit()

            self.assertEqual(response.status_code, 200)
            self.assertIsInstance(data, list)
            self.assertEqual(len(data), 15)

    def test_get_chambres_non_existing_hotel(self):
        with self.client:
            response = self.client.get('/chambres?hotel_id=999')

            self.assertEqual(response.status_code, 200)
            data = response.get_json()

            self.assertIsInstance(data, list)
            self.assertEqual(len(data), 0)

class TestChambresPost(unittest.TestCase):
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

    def test_create_chambres_as_admin(self):
        with self.client:
            hotel_obj = hotel(name="Hotel ABC", location="City XYZ", description="A luxurious hotel")
            db.session.add(hotel_obj)
            db.session.commit()

            chambre_body= {"numero": "101", "nb_personne": 2, "hotel_id": hotel_obj.id}

            response = self.client.post('/chambres', json=chambre_body, headers={'Authorization': f'Bearer {self.admin_token}'})
            data = response.get_json()
            chambres_obj = chambres.query.get(data["id"])
            db.session.delete(chambres_obj)
            db.session.delete(hotel_obj)
            db.session.commit()
            
            self.assertEqual(response.status_code, 201)
            self.assertIsInstance(data, dict)
            self.assertEqual(data['numero'], '101')

    def test_create_chambres_missing_json(self):
        with self.client:
            response = self.client.post('/chambres', json={},headers={'Authorization': f'Bearer {self.admin_token}'})
            data = response.get_json()

            self.assertEqual(response.status_code, 400)
            self.assertIn('error', data)
            self.assertEqual(data['error'], 'json not found')

    def test_create_chambres_unauthorized(self):
        with self.client:
            chambre_body = {"numero": "101", "nb_personne": 2, "hotel_id": 1}

            response = self.client.post('/chambres', json=chambre_body, headers={'Authorization': f'Bearer {self.user_token}'})
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

class TestChambresPut(unittest.TestCase):
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

    def test_put_chambres_as_admin(self):
        with self.client:
            hotel_obj = hotel(name="Hotel ABC", location="City XYZ", description="A luxurious hotel")
            db.session.add(hotel_obj)
            db.session.commit()

            chambre_body= {"numero": "101", "nb_personne": 2, "hotel_id": hotel_obj.id}
            response = self.client.post('/chambres', json=chambre_body, headers={'Authorization': f'Bearer {self.admin_token}'})
            data = response.get_json()
            
            chambre_body= {"numero": "102", "nb_personne": 2}
            response = self.client.put('/chambres/'+str(data["id"]), json=chambre_body, headers={'Authorization': f'Bearer {self.admin_token}'})
            data = response.get_json()

            chambres_obj = chambres.query.get(data["id"])
            db.session.delete(chambres_obj)
            db.session.delete(hotel_obj)
            db.session.commit()
            
            self.assertEqual(response.status_code, 200)
            self.assertIsInstance(data, dict)
            self.assertEqual(data['numero'], '102')

    def test_put_chambres_missing_json(self):
        with self.client:
            response = self.client.put('/chambres/1', json={},headers={'Authorization': f'Bearer {self.admin_token}'})
            data = response.get_json()

            self.assertEqual(response.status_code, 400)
            self.assertIn('error', data)
            self.assertEqual(data['error'], 'json not found')

    def test_put_chambres_unauthorized(self):
        with self.client:
            chambre_body = {"numero": "101", "nb_personne": 2, "hotel_id": 1}

            response = self.client.put('/chambres/2', json=chambre_body, headers={'Authorization': f'Bearer {self.user_token}'})
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

class TestDeleteChambres(unittest.TestCase):
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

    def test_delete_chambres_as_admin(self):
        with self.client:
            hotel_obj = hotel(name="Hotel ABC", location="City XYZ", description="A luxurious hotel")
            db.session.add(hotel_obj)
            db.session.commit()
            chambre = chambres(numero="101", nb_personne=2, hotel_id=hotel_obj.id)
            db.session.add(chambre)
            db.session.commit()

            response = self.client.delete(f'/chambres/{chambre.id}', headers={'Authorization': f'Bearer {self.admin_token}'})
            
            chambre_obj= chambres.query.get(chambre.id)
            db.session.delete(chambre)
            db.session.delete(hotel_obj)
            db.session.commit()

            self.assertEqual(response.status_code, 200)
            self.assertIsNone(chambre_obj)

    def test_delete_chambres_non_existing(self):
        with self.client:
            response = self.client.delete('/chambres/999', headers={'Authorization': f'Bearer {self.admin_token}'})
            data = response.get_json()

            self.assertEqual(response.status_code, 404)
            self.assertIn('error', data)
            self.assertEqual(data['error'], 'hotel not found')

    def test_delete_chambres_unauthorized(self):
        with self.client:
            response = self.client.delete(f'/chambres/2', headers={'Authorization': f'Bearer {self.user_token}'})
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



if __name__ == '__main__':
    unittest.main()
    app.run()