import unittest
from app.routes import app ,db
from app.models import Image

class TestimageGet(unittest.TestCase):
    def setUp(self):
        app.testing = True
        self.app_context = app.app_context()
        self.app_context.push()
        self.client = app.test_client()

if __name__ == '__main__':
    unittest.main()
    app.run()