import unittest
from selenium import webdriver
from selenium.webdriver.common.by import By

class TestAdmin(unittest.TestCase):
    def setUp(self):
        self.driver = webdriver.Chrome()
        self.driver.implicitly_wait(10)
        self.driver.get('http://localhost:5001')

    def tearDown(self):
        self.driver.quit()

    def test_access_local_server(self):

        title = self.driver.title
        self.assertIn('Home', title)


if __name__ == '__main__':
    unittest.main()