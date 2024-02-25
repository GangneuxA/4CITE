import unittest
from app import create_app ,db
from app.models import user
from dotenv import load_dotenv

class TestUserRoute(unittest.TestCase):
    def setUp(self):
        load_dotenv()
        app = create_app('testing')
        self.app_context = app.app_context()
        self.app_context.push()
        self.client = app.test_client()

    def login_user(self, email, password):
        # Simuler l'authentification en envoyant une requête POST à la route /login avec les identifiants de l'utilisateur
        response = self.client.post('/login', json={'email': email, 'password': password})
        print(response.status_code)
        return response.json['access_token']

    def test_get_user_as_employee(self):
        with self.client:
            employee = user(pseudo="sored", email='employee', role='employee')
            employee.set_password('password')
            db.session.add(employee)
            db.session.commit()

            token = self.login_user('employee', 'password')

            response = self.client.get('/user', headers={'Authorization': f'Bearer {token}'})
            data = response.get_json()

            self.assertEqual(response.status_code, 200)
            self.assertTrue(isinstance(data, list))
            self.assertTrue(len(data) > 0)
            db.session.delete(employee)
            db.session.commit()

    def test_get_user_as_regular_user(self):
        with self.client:
            user = user(email='user', role='user')
            user.save_to_db()

            # Authentifier l'utilisateur et obtenir le cookie de session
            cookie = self.login_user('user', 'password')

            # Effectuer une requête GET sur la route /user avec le cookie de session
            response = self.client.get('/user', headers={'Cookie': cookie})
            data = response.get_json()

            # Vérifier que la réponse est un succès et contient les détails de l'utilisateur actuel
            self.assertEqual(response.status_code, 200)
            self.assertTrue(isinstance(data, list))
            self.assertEqual(len(data), 1)

    def test_unauthorized_access(self):
        with self.client:
            # Effectuer une requête GET sur la route /user sans authentification
            response = self.client.get('/user')
            data = response.get_json()

            # Vérifier que la réponse est une erreur d'accès non autorisé (401 Unauthorized)
            self.assertEqual(response.status_code, 404)

if __name__ == '__main__':
    unittest.main()