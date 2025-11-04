from django.test import  TestCase
from django.contrib.auth import  get_user_model
from django.urls import  reverse

from rest_framework.test import APIClient
from rest_framework import status

REGISTER_USER_URL = reverse('authentication:register')
LOGIN_USER_URL = reverse('authentication:login')

def create_user(**params):
    """Create and return a new User"""
    return get_user_model().objects.create_user(**params)

class UserAuthTest(TestCase):
    def setUp(self):
        self.client = APIClient()
    def test_register_user(self):
        """
        1. Create a new user
        2. Check that the new user is created
        3. Check that a password is correct
        4. Check that the password is not in response
        """

    def test_user_email_already_exists(self):
        """
        1. Create a new user
        2. Check make a post request to be create endpoint
        """
    def test_non_exiting_user_cannot_login(self):
        """
        Test a user without account cannot login
        1. make a post request of to login
        """

    def test_existing_user_can_login(selfs):
        """
        Test an existing user can login
        1. create a user
        2. make a post request to login endpoint
        3. confirm status code if successful
        4. confirm payload
        """
