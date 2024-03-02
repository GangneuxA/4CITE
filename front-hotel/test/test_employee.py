import time
import unittest
from selenium import webdriver
from selenium.webdriver.common.by import By

class TestEmployee(unittest.TestCase):
    def setUp(self):
        self.driver = webdriver.Chrome()
        self.driver.implicitly_wait(10)
        self.driver.get('http://localhost:5001')

    def tearDown(self):
        self.driver.quit()

    def test_list_user(self):

        self.driver.get('http://localhost:5001/login')

        email_input = self.driver.find_element(By.NAME,'email' )
        email_input.send_keys('employee.employee@employee.fr')

        password_input = self.driver.find_element(By.NAME,'password' )
        password_input.send_keys('employee')

        submit_button = self.driver.find_element(By.NAME,'submit' )
        submit_button.click()
        time.sleep(2)

        self.assertIn('Home', self.driver.title)

        administration_button = self.driver.find_element(By.NAME,'administration' )
        administration_button.click()

        self.assertIn('Administration', self.driver.title)

        logout_button = self.driver.find_element(By.NAME,'logout' )
        logout_button.click()
        time.sleep(2)

        self.assertIn('Home', self.driver.title)

if __name__ == '__main__':
    unittest.main()