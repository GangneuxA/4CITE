import unittest
from app.routes import app ,db
from app.models import booking

class TestbookingGet(unittest.TestCase):
    def setUp(self):
        app.testing = True
        self.app_context = app.app_context()
        self.app_context.push()
        self.client = app.test_client()

if __name__ == '__main__':
    unittest.main()
    app.run()