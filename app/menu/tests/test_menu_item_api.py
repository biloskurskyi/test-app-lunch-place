from django.test import TestCase
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient

from user.tests.test_user_api import UserApiTestsBase


class MenuItemApiTestsForEmployeeUser(UserApiTestsBase, TestCase):
    """Test the features of the menu(MenuItemView) API."""

    def setUp(self):
        super().setUp()
        self.menu_url = reverse('menu:menu')
        self.menu_data = {
            "menu": "pizza",
            "day": 4
        }

    def create_menu_item(self):
        """
        Helper method to create a menu item and return its ID.
        """
        self.register_user(user_type=1)
        token = self.get_token()
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {token}')
        response = self.client.post(self.menu_url, self.menu_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        return response.data['id']

    def get_menu_item(self, menu_item_id):
        """
        Helper method to get a menu item by ID.
        """
        get_url = reverse('menu:menuItem', kwargs={'pk': menu_item_id})
        return self.client.get(get_url, format='json')

    def update_menu_item(self, menu_item_id, new_data):
        """
        Helper method to update a menu item by ID.
        """
        put_url = reverse('menu:menuItem', kwargs={'pk': menu_item_id})
        return self.client.put(put_url, new_data, format='json')

    def delete_menu_item(self, menu_item_id):
        """
        Helper method to delete a menu item by ID.
        """
        put_url = reverse('menu:menuItem', kwargs={'pk': menu_item_id})
        return self.client.delete(put_url, format='json')

    def test_get_menu_item_for_restaurant(self):
        """
        Ensure restaurant can get their item menu.
        """
        menu_item_id = self.create_menu_item()
        response = self.get_menu_item(menu_item_id)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_get_wrong_menu_item_for_restaurant(self):
        """
        Ensure restaurant cannot get a non-existent item menu.
        """
        menu_item_id = self.create_menu_item()
        response = self.get_menu_item(menu_item_id + 1)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_put_menu_item_for_restaurant(self):
        """
        Ensure restaurant can update their item menu.
        """
        menu_item_id = self.create_menu_item()
        new_data = {
            "menu": "borsh",
            "day": 4
        }
        response = self.update_menu_item(menu_item_id, new_data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['menu'], new_data['menu'])

    def test_delete_menu_item_for_restaurant(self):
        """
        Ensure restaurant can delete their item menu.
        """
        menu_item_id = self.create_menu_item()
        response = self.delete_menu_item(menu_item_id)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertIn('message', response.data)
        self.assertEqual(response.data['message'], 'Delete successful!')
