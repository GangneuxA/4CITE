import time
import unittest
import os
from selenium import webdriver
from selenium.webdriver.common.by import By

class TestAdmin(unittest.TestCase):
    def setUp(self):
        self.driver = webdriver.Chrome()
        self.driver.implicitly_wait(10)
        self.driver.get('http://localhost:5001')

    def tearDown(self):
        self.driver.quit()

    def test01_admin_create(self):

        self.driver.get('http://localhost:5001/login')

        email_input = self.driver.find_element(By.NAME,'email' )
        email_input.send_keys('admin.admin@admin.fr')

        password_input = self.driver.find_element(By.NAME,'password' )
        password_input.send_keys('admin')

        submit_button = self.driver.find_element(By.NAME,'submit' )
        submit_button.click()
        time.sleep(2)

        self.assertIn('Home', self.driver.title)

        administration_button = self.driver.find_element(By.NAME,'administration' )
        administration_button.click()

        self.assertIn('Administration', self.driver.title)

        admin_hotels_button = self.driver.find_element(By.NAME,'admin_hotels' )
        admin_hotels_button.click()
        time.sleep(2)

        self.assertIn('Admin_hotels', self.driver.title)

        admin_create_hotels_button = self.driver.find_element(By.NAME,'create_hotel' )
        admin_create_hotels_button.click()

        self.assertIn('Hotel', self.driver.title)

        name_input = self.driver.find_element(By.NAME,'name' )
        name_input.send_keys('HotelTest')

        description_input = self.driver.find_element(By.NAME,'description' )
        description_input.send_keys('descriptiontest')

        location_input = self.driver.find_element(By.NAME,'location' )
        location_input.send_keys('Tours')

        submit_button = self.driver.find_element(By.NAME,'submit' )
        submit_button.click()
        time.sleep(2)

        self.assertIn('Admin_hotels', self.driver.title)

        admin_create_room_button = self.driver.find_element(By.NAME,'create_room' )
        admin_create_room_button.click()

        self.assertIn('Rooms', self.driver.title)

        number_input = self.driver.find_element(By.NAME,'numero' )
        number_input.send_keys(666)

        nb_personne_input = self.driver.find_element(By.NAME,'nb_personne' )
        nb_personne_input.send_keys(2)

        submit_button = self.driver.find_element(By.NAME,'submit' )
        submit_button.click()
        time.sleep(2)

        self.assertIn('Admin_rooms', self.driver.title)

        administration_button = self.driver.find_element(By.NAME,'administration' )
        administration_button.click()

        self.assertIn('Administration', self.driver.title)

        admin_images_button = self.driver.find_element(By.NAME,'admin_images' )
        admin_images_button.click()

        self.assertIn('Images', self.driver.title)

        script_directory = os.path.dirname(os.path.abspath(__file__))

        image_path = os.path.join(script_directory, 'image_test.jpg')

        image_input = self.driver.find_element(By.NAME,'image' )
        image_input.send_keys(image_path)
        
        submit_button = self.driver.find_element(By.NAME,'submit_add' )
        submit_button.click()
        time.sleep(2)

        self.assertIn('Images', self.driver.title)

        logout_button = self.driver.find_element(By.NAME,'logout' )
        logout_button.click()
        time.sleep(2)

        self.assertIn('Home', self.driver.title)


    def test02_admin_update(self):

        self.driver.get('http://localhost:5001/login')

        email_input = self.driver.find_element(By.NAME,'email' )
        email_input.send_keys('admin.admin@admin.fr')

        password_input = self.driver.find_element(By.NAME,'password' )
        password_input.send_keys('admin')

        submit_button = self.driver.find_element(By.NAME,'submit' )
        submit_button.click()
        time.sleep(2)

        self.assertIn('Home', self.driver.title)

        administration_button = self.driver.find_element(By.NAME,'administration' )
        administration_button.click()

        self.assertIn('Administration', self.driver.title)

        admin_rooms_button = self.driver.find_element(By.NAME,'admin_rooms' )
        admin_rooms_button.click()

        self.assertIn('Admin_rooms', self.driver.title)

        admin_change_rooms_button = self.driver.find_element(By.NAME,'change_room' )
        admin_change_rooms_button.click()

        self.assertIn('Change Room', self.driver.title)

        nb_personne_input = self.driver.find_element(By.NAME,'nb_personne' )
        nb_personne_input.send_keys(6)

        submit_button = self.driver.find_element(By.NAME,'submit' )
        submit_button.click()
        time.sleep(2)

        self.assertIn('Admin_rooms', self.driver.title)

        administration_button = self.driver.find_element(By.NAME,'administration' )
        administration_button.click()

        self.assertIn('Administration', self.driver.title)

        admin_hotels_button = self.driver.find_element(By.NAME,'admin_hotels' )
        admin_hotels_button.click()
        time.sleep(2)

        self.assertIn('Admin_hotels', self.driver.title)

        admin_change_hotels_button = self.driver.find_element(By.NAME,'change_hotel' )
        admin_change_hotels_button.click()

        self.assertIn('Change Hotel', self.driver.title)

        name_input = self.driver.find_element(By.NAME,'name' )
        name_input.send_keys('HotelTestModif')

        submit_button = self.driver.find_element(By.NAME,'submit' )
        submit_button.click()
        time.sleep(2)

        self.assertIn('Admin_hotels', self.driver.title)

        logout_button = self.driver.find_element(By.NAME,'logout' )
        logout_button.click()
        time.sleep(2)

        self.assertIn('Home', self.driver.title)

    def test03_user_booking_and_admin_update_delete(self):

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

        login_button = self.driver.find_element(By.NAME,'login' )
        login_button.click()
        
        self.assertIn('Login', self.driver.title)

        email_input = self.driver.find_element(By.NAME,'email' )
        email_input.send_keys('admin.admin@admin.fr')

        password_input = self.driver.find_element(By.NAME,'password' )
        password_input.send_keys('admin')

        submit_button = self.driver.find_element(By.NAME,'submit' )
        submit_button.click()
        time.sleep(2)

        self.assertIn('Home', self.driver.title)

        administration_button = self.driver.find_element(By.NAME,'administration' )
        administration_button.click()

        self.assertIn('Administration', self.driver.title)

        admin_booking = self.driver.find_element(By.NAME,'admin_bookings' )
        admin_booking.click()

        self.assertIn('Admin_bookings', self.driver.title)

        admin_change_booking = self.driver.find_element(By.NAME,'change_booking' )
        admin_change_booking.click()

        self.assertIn('Change Booking', self.driver.title)

        dateout_input = self.driver.find_element(By.NAME,'dateout' )
        dateout_input.send_keys('2024-09-05')

        submit_button = self.driver.find_element(By.NAME,'submit' )
        submit_button.click()
        time.sleep(2)

        self.assertIn('Admin_bookings', self.driver.title)
        time.sleep(2)

        admin_delete_booking = self.driver.find_element(By.NAME,'delete_booking' )
        admin_delete_booking.click()
        time.sleep(2)

        self.assertIn('Admin_bookings', self.driver.title)
        time.sleep(2)

        logout_button = self.driver.find_element(By.NAME,'logout' )
        logout_button.click()
        time.sleep(2)

        self.assertIn('Home', self.driver.title)

    def test04_admin_delete(self):

        self.driver.get('http://localhost:5001/login')

        email_input = self.driver.find_element(By.NAME,'email' )
        email_input.send_keys('admin.admin@admin.fr')

        password_input = self.driver.find_element(By.NAME,'password' )
        password_input.send_keys('admin')

        submit_button = self.driver.find_element(By.NAME,'submit' )
        submit_button.click()
        time.sleep(2)

        self.assertIn('Home', self.driver.title)

        administration_button = self.driver.find_element(By.NAME,'administration' )
        administration_button.click()

        self.assertIn('Administration', self.driver.title)

        admin_rooms_button = self.driver.find_element(By.NAME,'admin_rooms' )
        admin_rooms_button.click()

        self.assertIn('Admin_rooms', self.driver.title)

        admin_delete_rooms_button = self.driver.find_element(By.NAME,'delete_room' )
        admin_delete_rooms_button.click()

        self.assertIn('Admin_rooms', self.driver.title)
        time.sleep(2)

        administration_button = self.driver.find_element(By.NAME,'administration' )
        administration_button.click()

        self.assertIn('Administration', self.driver.title)

        admin_images_button = self.driver.find_element(By.NAME,'admin_images' )
        admin_images_button.click()

        self.assertIn('Images', self.driver.title)

        admin_delete_images_button = self.driver.find_element(By.NAME,'submit_delete' )
        admin_delete_images_button.click()

        self.assertIn('Images', self.driver.title)
        time.sleep(2)

        administration_button = self.driver.find_element(By.NAME,'administration' )
        administration_button.click()

        self.assertIn('Administration', self.driver.title)

        admin_hotels_button = self.driver.find_element(By.NAME,'admin_hotels' )
        admin_hotels_button.click()
        time.sleep(2)

        self.assertIn('Admin_hotels', self.driver.title)

        admin_delete_hotels_button = self.driver.find_element(By.NAME,'delete_hotel' )
        admin_delete_hotels_button.click()

        self.assertIn('Admin_hotels', self.driver.title)
        time.sleep(2)

        logout_button = self.driver.find_element(By.NAME,'logout' )
        logout_button.click()
        time.sleep(2)

        self.assertIn('Home', self.driver.title)


if __name__ == '__main__':
    unittest.main()