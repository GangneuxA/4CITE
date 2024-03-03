import unittest
from selenium import webdriver
from selenium.webdriver.common.by import By

class TestAnonymous(unittest.TestCase):
    def setUp(self):
        self.driver = webdriver.Chrome()
        self.driver.implicitly_wait(10)
        self.driver.get('http://localhost:5001')

    def tearDown(self):
        self.driver.quit()

    def test01_access_local_server(self):

        title = self.driver.title
        self.assertIn('Home', title)

    def test02_access_login_page(self):

        login_button = self.driver.find_element(By.NAME,'login' )
        login_button.click()

        title = self.driver.title
        self.assertIn('Login', title)

    def test03_access_register_page(self):

        register_button = self.driver.find_element(By.NAME,'register' )
        register_button.click()

        title = self.driver.title
        self.assertIn('Register', title)

    def test04_access_reservations_page(self):

        reservations_button = self.driver.find_element(By.NAME,'reservations' )
        reservations_button.click()

        title = self.driver.title
        self.assertIn('Login', title)

    def test05_access_profil_page(self):

        profil_button = self.driver.find_element(By.NAME,'profil' )
        profil_button.click()

        title = self.driver.title
        self.assertIn('Login', title)

if __name__ == '__main__':
    unittest.main()