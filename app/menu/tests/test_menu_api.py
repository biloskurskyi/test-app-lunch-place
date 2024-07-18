from django.test import TestCase
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient

from user.tests.test_user_api import UserApiTestsBase


class MenuApiTestsForEmployeeUser(UserApiTestsBase, TestCase):
    """Test the features of the menu(MenuView) API."""

    def setUp(self):
        super().setUp()
        self.menu_url = reverse('menu:menu')
        self.menu_data = {
            "menu": "pizza",
            "day": 4
        }

    def test_post_menu(self):
        """
        Ensure we can create a new menu if we are restaurant user
        """
        self.register_user(user_type=1)
        token = self.get_token()
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {token}')
        response = self.client.post(self.menu_url, self.menu_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_error_post_menu(self):
        """
        Ensure we can not create a new menu if we are not restaurant user
        """
        self.register_user()
        token = self.get_token()
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {token}')
        response = self.client.post(self.menu_url, self.menu_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('message', response.data)
        self.assertEqual(response.data['message'], 'This user has not this permission')

    def test_get_menu_for_restaurant(self):
        """
        Ensure restaurant can get their whole menu
        """
        self.register_user(user_type=1)
        token = self.get_token()
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {token}')
        response = self.client.get(self.menu_url, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_get_menu_for_employee(self):
        """
        Ensure employee can get menu for today
        """
        self.register_user()
        token = self.get_token()
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {token}')
        response = self.client.get(self.menu_url, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
