import time
import unittest
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys

class TestUsers(unittest.TestCase):
    def setUp(self):
        self.driver = webdriver.Chrome()
        self.driver.implicitly_wait(10)
        self.driver.get('http://localhost:5001')

    def tearDown(self):
        self.driver.quit()

    def test01_user_profil(self):
        print("test_user_profil")
        register_button = self.driver.find_element(By.NAME,'register' )
        register_button.click()

        pseudo_input = self.driver.find_element(By.NAME,'pseudo' )
        pseudo_input.send_keys('USerSelenium')

        email_input = self.driver.find_element(By.NAME,'email' )
        email_input.send_keys('Selenium@email.com')

        password_input = self.driver.find_element(By.NAME,'password' )
        password_input.send_keys('selenium')

        confirm_password_input = self.driver.find_element(By.NAME,'confirm_password' )
        confirm_password_input.send_keys('selenium')

        submit_button = self.driver.find_element(By.NAME,'submit' )
        submit_button.click()
        time.sleep(2)

        self.assertIn('Login', self.driver.title)

        email_input = self.driver.find_element(By.NAME,'email' )
        email_input.send_keys('Selenium@email.com')

        password_input = self.driver.find_element(By.NAME,'password' )
        password_input.send_keys('selenium')

        submit_button = self.driver.find_element(By.NAME,'submit' )
        submit_button.click()
        time.sleep(2)

        self.assertIn('Home', self.driver.title)

        profil_button = self.driver.find_element(By.NAME, 'profil')
        profil_button.click()

        self.assertIn('User', self.driver.title)

        profil_button = self.driver.find_element(By.NAME, 'modified')
        profil_button.click()

        self.assertIn('Change User', self.driver.title)

        pseudo_input = self.driver.find_element(By.NAME,'pseudo' )
        pseudo_input.send_keys('UpdateUserPseudo')

        submit_button = self.driver.find_element(By.NAME,'submit' )
        submit_button.click()
        time.sleep(2)

        self.assertIn('User', self.driver.title)
        time.sleep(2)

        profil_button = self.driver.find_element(By.NAME, 'delete')
        profil_button.click()

        self.assertIn('Home', self.driver.title)

    def test02_user_booking(self):
        print("test_user_booking")
        self.driver.get('http://localhost:5001/login')

        email_input = self.driver.find_element(By.NAME,'email' )
        email_input.send_keys('user.user@user.fr')

        password_input = self.driver.find_element(By.NAME,'password' )
        password_input.send_keys('user')

        submit_button = self.driver.find_element(By.NAME,'submit' )
        submit_button.click()
        time.sleep(2)

        self.assertIn('Home', self.driver.title)

        booking_button = self.driver.find_element(By.NAME, 'booking')
        booking_button.click()

        self.assertIn('Booking', self.driver.title)

        datein_input = self.driver.find_element(By.NAME,'datein' )
        datein_input.send_keys('2026-06-05')

        dateout_input = self.driver.find_element(By.NAME,'dateout' )
        dateout_input.send_keys('2026-06-15')

        submit_button = self.driver.find_element(By.NAME,'submit' )
        submit_button.click()
        time.sleep(2)

        self.assertIn('Reservations', self.driver.title)

        logout_button = self.driver.find_element(By.NAME,'logout' )
        logout_button.click()
        time.sleep(2)

        self.assertIn('Home', self.driver.title)

    def test03_user_update_booking(self):
            print("test_user_update_booking")
            self.driver.get('http://localhost:5001/login')

            email_input = self.driver.find_element(By.NAME,'email' )
            email_input.send_keys('user.user@user.fr')

            password_input = self.driver.find_element(By.NAME,'password' )
            password_input.send_keys('user')

            submit_button = self.driver.find_element(By.NAME,'submit' )
            submit_button.click()
            time.sleep(2)

            self.assertIn('Home', self.driver.title)

            booking_button = self.driver.find_element(By.NAME, 'reservations')
            booking_button.click()

            self.assertIn('Reservations', self.driver.title)

            modified_button = self.driver.find_element(By.NAME,'modified' )
            modified_button.click()

            self.assertIn('Change Booking', self.driver.title)

            dateout_input = self.driver.find_element(By.NAME,'dateout' )
            dateout_input.send_keys('2026-06-20')

            submit_button = self.driver.find_element(By.NAME,'submit' )
            submit_button.click()
            time.sleep(2)

            self.assertIn('Reservations', self.driver.title)

            logout_button = self.driver.find_element(By.NAME,'logout' )
            logout_button.click()
            time.sleep(2)

            self.assertIn('Home', self.driver.title)

    def test04_user_delete_booking(self):
            print("test_user_delete_booking")
            self.driver.get('http://localhost:5001/login')

            email_input = self.driver.find_element(By.NAME,'email' )
            email_input.send_keys('user.user@user.fr')

            password_input = self.driver.find_element(By.NAME,'password' )
            password_input.send_keys('user')

            submit_button = self.driver.find_element(By.NAME,'submit' )
            submit_button.click()
            time.sleep(2)

            self.assertIn('Home', self.driver.title)

            booking_button = self.driver.find_element(By.NAME, 'reservations')
            booking_button.click()

            self.assertIn('Reservations', self.driver.title)

            modified_button = self.driver.find_element(By.NAME,'delete' )
            modified_button.click()

            self.assertIn('Reservations', self.driver.title)

            logout_button = self.driver.find_element(By.NAME,'logout' )
            logout_button.click()
            time.sleep(2)

            self.assertIn('Home', self.driver.title)

if __name__ == '__main__':
    unittest.main()