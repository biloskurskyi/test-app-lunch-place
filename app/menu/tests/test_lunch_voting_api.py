from django.test import TestCase
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient

from core.models import Lunch, LunchVoting, User


class LunchVotingTests(TestCase):
    """Test the features of the lunch voting API."""

    def setUp(self):
        self.client = APIClient()
        self.register_url = reverse('user:register')
        self.login_url = reverse('user:login')
        self.menu_url = reverse('menu:menu')
        self.vote_url = lambda pk: reverse('menu:voteItem', kwargs={'pk': pk})
        self.user_data = {
            'name': 'testuser',
            'password': 'testpassword123',
            'email': 'testuser@test.com',
            'user_type': 0,  # Employee user
        }
        self.menu_data = {
            "menu": "pizza",
            "day": 4
        }

    def register_user(self, **kwargs):
        """Helper method to register a user."""
        data = self.user_data.copy()
        data.update(kwargs)
        return self.client.post(self.register_url, data, format='json')

    def login_user(self, **kwargs):
        """Helper method to log in a user."""
        data = {
            'email': self.user_data['email'],
            'password': self.user_data['password'],
        }
        data.update(kwargs)
        return self.client.post(self.login_url, data, format='json')

    def get_token(self, email, password):
        """Helper method to get token."""
        response = self.client.post(self.login_url, {'email': email, 'password': password})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        return response.data['jwt']

    def create_menu_item(self):
        """Helper method to create a menu item."""
        self.register_user(email='restaurant@test.com', user_type=1)
        token = self.get_token('restaurant@test.com', 'testpassword123')
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {token}')
        response = self.client.post(self.menu_url, self.menu_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        return response.data['id']

    def test_post_lunch_voting(self):
        """
        Ensure user can vote for a menu item
        """
        menu_item_id = self.create_menu_item()
        self.register_user(email='employee@test.com', user_type=0)
        token = self.get_token('employee@test.com', 'testpassword123')
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {token}')

        vote_url = self.vote_url(menu_item_id)
        response = self.client.post(vote_url, format='json')

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['message'], "Vote cast successfully")

        vote = LunchVoting.objects.filter(user=User.objects.get(email='employee@test.com'),
                                          lunch_id=menu_item_id).first()
        self.assertIsNotNone(vote)
