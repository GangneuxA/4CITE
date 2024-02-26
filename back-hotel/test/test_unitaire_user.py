import unittest
from app.routes import app ,db
from app.models import user

class TestUserGet(unittest.TestCase):
    def setUp(self):
        app.testing = True
        self.app_context = app.app_context()
        self.app_context.push()
        self.client = app.test_client()

    def test_get_user_as_employee(self):
        with self.client:
            employee = user(pseudo="sored", email='employee', role='employee')
            employee.set_password('password')
            db.session.add(employee)
            db.session.commit()

            token = self.login_user('employee', 'password')

            response = self.client.get('/user', headers={'Authorization': f'Bearer {token}'})
            data = response.get_json()
            db.session.delete(employee)
            db.session.commit()

            self.assertEqual(response.status_code, 200)
            self.assertTrue(isinstance(data, list))
            self.assertTrue(len(data) > 0)


    def test_get_user_as_regular_user(self):
        with self.client:
            user_obj = user(pseudo="sored",email='user', role='user')
            user_obj.set_password('password')
            db.session.add(user_obj)
            db.session.commit()

            token = self.login_user('user', 'password')

            response = self.client.get('/user', headers={'Authorization': f'Bearer {token}'})
            data = response.get_json()

            db.session.delete(user_obj)
            db.session.commit()
            self.assertEqual(response.status_code, 200)
            self.assertTrue(isinstance(data, list))
            self.assertEqual(len(data), 1)


    def test_unauthorized_access(self):
        with self.client:
            response = self.client.get('/user')
            self.assertEqual(response.status_code, 401)

    #function to connect
    def login_user(self, email, password):
        response = self.client.post('/login', json={'email': email, 'password': password}, content_type='application/json')
        data = response.get_json()
        return data['access_token']
    
class TestUserPost(unittest.TestCase):
    def setUp(self):
        app.testing = True
        self.app_context = app.app_context()
        self.app_context.push()
        self.client = app.test_client()

    def test_create_user(self):
        with self.client:
            user_data = {
                'pseudo': 'test_user',
                'email': 'test@example.com',
                'password': 'test_password'
            }
            response = self.client.post('/user', json=user_data)
            data = response.get_json()
            created_user = user.query.filter_by(email=user_data['email']).first()
            self.assertIsNotNone(created_user)
            db.session.delete(created_user)
            db.session.commit()
            self.assertEqual(response.status_code, 201)
            self.assertEqual(data['pseudo'], user_data['pseudo'])
            self.assertEqual(data['email'], user_data['email'])
            

    def test_create_user_without_json(self):
        with self.client:
            response = self.client.post('/user')
            data = response.get_json()

            self.assertEqual(response.status_code, 415)

    def test_create_user_missing_parameter(self):
        with self.client:
            user_data = {
                'pseudo': 'test_user',
                'password': 'test_password'
            }
            response = self.client.post('/user', json=user_data)
            data = response.get_json()

            self.assertEqual(response.status_code, 400)
            self.assertIn('error', data)
            self.assertEqual(data['error'], 'missing parameter')


class TestUserPut(unittest.TestCase):
    def setUp(self):
        app.testing = True
        self.app_context = app.app_context()
        self.app_context.push()
        self.client = app.test_client()

    def test_update_user(self):
        with self.client:
            user_obj = user(pseudo="test_user", email="test@example.com")
            user_obj.set_password('password')
            db.session.add(user_obj)
            db.session.commit()

            token = self.login_user('test@example.com', 'password')

            updated_data = {
                'pseudo': 'updated_name',
                'email': 'updated@example.com',
                'password': 'updated_password'
            }

            response = self.client.put(f'/user/{user_obj.id}', json=updated_data, headers={'Authorization': f'Bearer {token}'})
            updated_user = user.query.get(user_obj.id)
            db.session.delete(updated_user)
            db.session.commit()

            self.assertEqual(response.status_code, 200)
            self.assertEqual(updated_user.pseudo, updated_data['pseudo'])
            self.assertEqual(updated_user.email, updated_data['email'])
            self.assertTrue(updated_user.check_password(updated_data['password']))

    def test_update_user_unauthorized(self):
        with self.client:
            user_obj = user(pseudo="test_user", email="test@example.com")
            user_obj.set_password('password')
            db.session.add(user_obj)

            user_obj2 = user(pseudo="test_user2", email="other@example.com")
            user_obj2.set_password('password')
            db.session.add(user_obj2)
            db.session.commit()


            token = self.login_user('other@example.com', 'password')

            updated_data = {
                'pseudo': 'updated_name',
                'email': 'updated@example.com',
                'password': 'updated_password'
            }
            response = self.client.put(f'/user/{user_obj.id}', json=updated_data, headers={'Authorization': f'Bearer {token}'})
            unchanged_user = user.query.get(user_obj.id)
            db.session.delete(user_obj)
            db.session.delete(user_obj2)
            db.session.commit()

            self.assertEqual(response.status_code, 404)
            self.assertEqual(unchanged_user.pseudo, user_obj.pseudo)
            self.assertEqual(unchanged_user.email, user_obj.email)

    def test_update_user_unauthenticated(self):
        with self.client:
            user_obj = user(pseudo="test_user", email="testun@example.com")
            user_obj.set_password('password')
            db.session.add(user_obj)
            db.session.commit()

            updated_data = {
                'pseudo': 'updated_name',
                'email': 'updated@example.com',
                'password': 'updated_password'
            }
            response = self.client.put(f'/user/{user_obj.id}', json=updated_data)
            unchanged_user = user.query.get(user_obj.id)
            db.session.delete(unchanged_user)
            db.session.commit()

            self.assertEqual(response.status_code, 401)
            self.assertEqual(unchanged_user.pseudo, user_obj.pseudo)
            self.assertEqual(unchanged_user.email, user_obj.email)

    def login_user(self, email, password):
        response = self.client.post('/login', json={'email': email, 'password': password}, content_type='application/json')
        data = response.get_json()
        return data['access_token']

class TestUserDelete(unittest.TestCase):
    def setUp(self):
        app.testing = True
        self.app_context = app.app_context()
        self.app_context.push()
        self.client = app.test_client()

    def test_delete_user(self):
        with self.client:
            user_obj = user(pseudo="test_user", email="test@example.com")
            user_obj.set_password('password')
            db.session.add(user_obj)
            db.session.commit()

            token = self.login_user('test@example.com', 'password')

            response = self.client.delete('/user', headers={'Authorization': f'Bearer {token}'})
            deleted_user = user.query.get(user_obj.id)

            self.assertEqual(response.status_code, 200)
            self.assertIsNone(deleted_user)

    def test_delete_user_not_found(self):
        with self.client:
            user_obj = user(pseudo="test_user", email="nonexistent@example.com")
            user_obj.set_password('password')
            db.session.add(user_obj)
            db.session.commit()

            token = self.login_user('nonexistent@example.com', 'password')
            db.session.delete(user_obj)
            db.session.commit()

            response = self.client.delete('/user', headers={'Authorization': f'Bearer {token}'})
            data = response.get_json()

            self.assertEqual(response.status_code, 404)
            self.assertIn('error', data)
            self.assertEqual(data['error'], 'user not found')

    def test_delete_user_unauthenticated(self):
        with self.client:
            response = self.client.delete('/user')
            self.assertEqual(response.status_code, 401)

    def login_user(self, email, password):
        response = self.client.post('/login', json={'email': email, 'password': password}, content_type='application/json')
        data = response.get_json()
        return data['access_token']

class TestLogout(unittest.TestCase):
    def setUp(self):
        app.testing = True
        self.app_context = app.app_context()
        self.app_context.push()
        self.client = app.test_client()

    def test_logout(self):
        with self.client:
            user_obj = user(pseudo="test_user", email="test@example.com")
            user_obj.set_password('password')
            db.session.add(user_obj)
            db.session.commit()
            token = self.login_user('test@example.com', 'password')

            response = self.client.post('/logout', headers={'Authorization': f'Bearer {token}'})
            data = response.get_json()
            db.session.delete(user_obj)
            db.session.commit()
            
            self.assertEqual(response.status_code, 200)
            self.assertIn('msg', data)
            self.assertEqual(data['msg'], 'logout successful')

    def test_logout_unauthenticated(self):
        with self.client:
            response = self.client.post('/logout')
            self.assertEqual(response.status_code, 401)

    def login_user(self, email, password):
        response = self.client.post('/login', json={'email': email, 'password': password}, content_type='application/json')
        data = response.get_json()
        return data['access_token']

class TestLogin(unittest.TestCase):
    def setUp(self):
        app.testing = True
        self.app_context = app.app_context()
        self.app_context.push()
        self.client = app.test_client()

    def test_login_successful(self):
        with self.client:
            user_obj = user(pseudo="test_user", email="test@example.com")
            user_obj.set_password('password')
            db.session.add(user_obj)
            db.session.commit()

            login_data = {
                'email': 'test@example.com',
                'password': 'password'
            }

            response = self.client.post('/login', json=login_data)
            data = response.get_json()
            db.session.delete(user_obj)
            db.session.commit()

            self.assertEqual(response.status_code, 200)
            self.assertIn('access_token', data)
            self.assertTrue(data['access_token'])

    def test_login_user_not_found(self):
        with self.client:
            login_data = {
                'email': 'nonexistent@example.com',
                'password': 'password'
            }

            response = self.client.post('/login', json=login_data)
            data = response.get_json()

            self.assertEqual(response.status_code, 404)
            self.assertIn('error', data)
            self.assertEqual(data['error'], 'user not found')

    def test_login_wrong_password(self):
        with self.client:
            user_obj = user(pseudo="test_user", email="test@example.com")
            user_obj.set_password('password')
            db.session.add(user_obj)
            db.session.commit()

            login_data = {
                'email': 'test@example.com',
                'password': 'wrong_password'
            }
            response = self.client.post('/login', json=login_data)
            data = response.get_json()
            db.session.delete(user_obj)
            db.session.commit()

            self.assertEqual(response.status_code, 400)
            self.assertIn('error', data)
            self.assertEqual(data['error'], 'password is wrong')

    def test_login_missing_json(self):
        with self.client:
            response = self.client.post('/login')
            self.assertEqual(response.status_code, 415)

if __name__ == '__main__':
    unittest.main()
    app.run()