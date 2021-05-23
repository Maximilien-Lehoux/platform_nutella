from django.test import TestCase
from django.urls import reverse
from selenium import webdriver
import time

from django.contrib.staticfiles.testing import StaticLiveServerTestCase
from django.contrib.auth.models import User


class MySeleniumTests(StaticLiveServerTestCase):

    @classmethod
    def setUp(self):
        self.driver = webdriver.Chrome("C:/Users/Maximilien/chromedriver.exe")
        self.user = User.objects.create(username='Arthur', last_name='H',
                                        email='arthurH@gmail.com')
        self.user.set_password('1234')
        self.user.save()

    def test_login(self):
        self.driver.get(str(self.live_server_url) + '/accounts/login')
        username_input = self.driver.find_element_by_id('id_user_name')
        password_input = self.driver.find_element_by_id('id_password')
        submission_button = self.driver.find_element_by_css_selector(
            '#button_login')
        username_input.send_keys('Arthur')
        password_input.send_keys('1234')
        submission_button.click()
        redirection_url = self.driver.current_url
        self.assertEqual(
            self.live_server_url + '/food/index/', redirection_url)

    def logo_disconnection(self):
        self.driver.get(str(self.live_server_url))
        login_button = self.driver.find_element_by_css_selector(
            '#click_click'
        )
        login_button.click()

    def disconnection(self):
        self.client.login(username="Arthur", password="1234")
        self.driver.get(str(self.live_server_url))
        disconnection_button = self.driver.find_element_by_css_selector(
            '#click_click'
        )
        disconnection_button.click()
        redirection_url = self.driver.current_url
        self.assertEqual(
            self.live_server_url + '/food/index/', redirection_url)


class TestViewsFood(TestCase):
    def setUp(self):
        self.user = User.objects.create(username='Arthur', last_name='H',
                                        email='arthurH@gmail.com')
        self.user.set_password('1234')
        self.user.save()

    def test_login_page_return_200(self):
        response = self.client.get(reverse('accounts:login_page'))
        self.assertEqual(response.status_code, 200)

    def test_login_page_return_200_with_log_invalid(self):
        data = {"user_name": "Merlin", "password": "1234"}
        response = self.client.get(reverse('accounts:login_page'), data)
        self.assertEqual(response.status_code, 200)

    def test_login_page_return_302_with_log_valid(self):
        data = {"user_name": "Arthur", "password": "1234"}
        response = self.client.post(reverse('accounts:login_page'), data)
        self.assertEqual(response.status_code, 302)

    def test_register_page_return_200(self):
        response = self.client.get(reverse('accounts:register'))
        self.assertEqual(response.status_code, 200)

    def test_register_page_return_302_with_form_valid(self):
        data = {"your_name": "Perceval", "email": "perceval@gmail.com",
                "password": "Chevaliertableronde",
                "password2": "Chevaliertableronde"}
        response = self.client.post(reverse('accounts:register'), data)
        self.assertEqual(response.status_code, 302)

    def test_icon_connection_page_return_200_with_login(self):
        self.client.login(username="Arthur", password="1234")
        response = self.client.get(reverse('accounts:connection_user'))
        self.assertEqual(response.status_code, 200)

    def test_icon_connection_page_return_302_without_login(self):
        self.client.logout()
        response = self.client.get(reverse('accounts:connection_user'))
        self.assertEqual(response.status_code, 302)

    def test_icon_disconnection_page_return_302_with_login(self):
        self.client.login(username="Arthur", password="1234")
        response = self.client.get(reverse('accounts:disconnection_user'))
        self.assertEqual(response.url, "/food/index/")
        self.assertEqual(response.status_code, 302)

    def test_icon_disconnection_page_return_302_without_login(self):
        self.client.logout()
        response = self.client.get(reverse('accounts:disconnection_user'))
        self.assertEqual(response.url, "/accounts/login/")
        self.assertEqual(response.status_code, 302)
