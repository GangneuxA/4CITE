import unittest
from app.routes import app ,db
from app.models import Image , hotel , user
import io
from PIL import Image as PILImage

class TestimageGet(unittest.TestCase):
    def setUp(self):
        app.testing = True
        self.app_context = app.app_context()
        self.app_context.push()
        self.client = app.test_client()

    def test_get_hotel_images_existing_hotel(self):
        with self.client:
            hotel_obj = hotel(name="Hotel ABC", location="City XYZ", description="A luxurious hotel")
            db.session.add(hotel_obj)
            db.session.commit()

            image1 = Image(name="image1.jpg",data=bytes("00101010", 'utf8'), hotel_id=hotel_obj.id)
            image2 = Image(name="image2.jpg",data=bytes("00101010", 'utf8'), hotel_id=hotel_obj.id)
            db.session.add_all([image1, image2])
            db.session.commit()

            response = self.client.get(f'/image/{hotel_obj.id}')
            data = response.get_json()
            db.session.delete(image1)
            db.session.delete(image2)
            db.session.delete(hotel_obj)
            db.session.commit()

            self.assertEqual(response.status_code, 200)
            self.assertTrue(isinstance(data, list))
            self.assertEqual(len(data), 2)

    def test_get_hotel_images_non_existing_hotel(self):
        with self.client:
            nonexistent_hotel_id = 9999
            response = self.client.get(f'/image/{nonexistent_hotel_id}')
            data = response.get_json()

            self.assertEqual(response.status_code, 404)
            self.assertIn('error', data)
            self.assertEqual(data['error'], 'Hotel not found')





class Testimagepost(unittest.TestCase):
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

    def test_upload_image_as_admin(self):
        with self.client:
            fake_image_data = PILImage.new('RGB', (100, 100)).tobytes()
            fake_image = io.BytesIO(fake_image_data)
            fake_image.name = 'test_image.jpg'

            hotel_obj = hotel(name="Hotel ABC", location="City XYZ", description="A luxurious hotel")
            db.session.add(hotel_obj)
            db.session.commit()

            response = self.client.post('/image', data={'image': (fake_image, 'test_image.jpg'), 'hotel_id': hotel_obj.id}, headers={'Authorization': f'Bearer {self.admin_token}'})
            data = response.get_json()
            image_obj = Image.query.filter_by(hotel_id=hotel_obj.id).first()
            db.session.delete(image_obj)
            db.session.delete(hotel_obj)
            db.session.commit()

            self.assertEqual(response.status_code, 200)
            self.assertIn('message', data)
            self.assertEqual(data['message'], 'Image uploaded successfully')

    def test_upload_image_unauthorized(self):
        with self.client:
            fake_image_data = PILImage.new('RGB', (100, 100)).tobytes()
            fake_image = io.BytesIO(fake_image_data)
            fake_image.name = 'test_image.jpg'

            response = self.client.post('/image', data={'image': (fake_image, 'test_image.jpg'), 'hotel_id': 1}, headers={'Authorization': f'Bearer {self.user_token}'})
            data = response.get_json()

            self.assertEqual(response.status_code, 404)
            self.assertIn('error', data)
            self.assertEqual(data['error'], 'You have not the permission for this')

    def test_upload_image_no_image_provided(self):
        with self.client:
            response = self.client.post('/image', data={'hotel_id': 1}, headers={'Authorization': f'Bearer {self.admin_token}'})
            data = response.get_json()

            self.assertEqual(response.status_code, 400)
            self.assertIn('error', data)
            self.assertEqual(data['error'], 'No image provided')

    def create_admin_user(self, name , mail , role):
        admin_user = user(pseudo=name, email=mail, role=role)
        admin_user.set_password("admin_password")
        db.session.add(admin_user)
        db.session.commit()
        response = self.client.post('/login', json={'email': mail, 'password': 'admin_password'})
        data = response.get_json()
        return data['access_token']

class TestImageDelete(unittest.TestCase):
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


    def test_delete_image_as_admin(self):
        with self.client:
            hotel_obj = hotel(name="Hotel ABC", location="City XYZ", description="A luxurious hotel")
            db.session.add(hotel_obj)
            db.session.commit()

            image = Image(name="test_image.jpg", data=b'Test image data', hotel_id=hotel_obj.id)
            db.session.add(image)
            db.session.commit()

            response = self.client.delete(f'/image/{hotel_obj.id}/{image.id}', headers={'Authorization': f'Bearer {self.admin_token}'})
            db.session.delete(hotel_obj)
            db.session.commit()

            self.assertEqual(response.status_code, 200)
            self.assertIsNone(Image.query.get(image.id))

    def test_delete_image_non_existing_hotel(self):
        with self.client:
            nonexistent_hotel_id = 9999

            response = self.client.delete(f'/image/{nonexistent_hotel_id}/1', headers={'Authorization': f'Bearer {self.admin_token}'})
            data = response.get_json()

            self.assertEqual(response.status_code, 404)
            self.assertIn('error', data)
            self.assertEqual(data['error'], 'Hotel not found')

    def test_delete_non_existing_image(self):
        with self.client:
            hotel_obj = hotel(name="Hotel ABC", location="City XYZ", description="A luxurious hotel")
            db.session.add(hotel_obj)
            db.session.commit()

            nonexistent_image_id = 9999

            response = self.client.delete(f'/image/{hotel_obj.id}/{nonexistent_image_id}', headers={'Authorization': f'Bearer {self.admin_token}'})
            data = response.get_json()
            db.session.delete(hotel_obj)
            db.session.commit()

            self.assertEqual(response.status_code, 404)
            self.assertIn('error', data)
            self.assertEqual(data['error'], 'Image not found for the specified hotel')

    def test_delete_image_unauthorized(self):
        with self.client:
            hotel_obj = hotel(name="Hotel ABC", location="City XYZ", description="A luxurious hotel")
            db.session.add(hotel_obj)
            db.session.commit()

            image = Image(name="test_image.jpg", data=b'Test image data', hotel_id=hotel_obj.id)
            db.session.add(image)
            db.session.commit()

            response = self.client.delete(f'/image/{hotel_obj.id}/{image.id}', headers={'Authorization': f'Bearer {self.user_token}'})
            data = response.get_json()

            db.session.delete(image)
            db.session.delete(hotel_obj)
            db.session.commit()


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