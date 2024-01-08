from django.test import TestCase
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient
from api.models import User
from api.serializers.user import UserSerializer

from tests.setup import create_admin, create_user
from tests.utils import perform_login


class UserListTests(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.url = reverse('user-list')

        # Create an admin user
        self.admin = create_admin('admin@example.com', '123')

        # Create a regular user
        self.user = create_user('user@example.com', '123')

    def test_list_users_as_admin(self):
        # GIVEN
        login_data = {'email': 'admin@example.com', 'password': '123'}
        login_response = perform_login(login_data)
        access_token = login_response.data['access']
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {access_token}')

        # WHEN
        response = self.client.get(self.url)

        # THEN
        users = User.objects.all()
        serializer = UserSerializer(users, many=True)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, serializer.data)
        self.assertEqual(len(response.data), 2)

    def test_list_users_as_regular_user(self):
        # GIVEN
        login_data = {'email': 'user@example.com', 'password': '123'}
        login_response = perform_login(login_data)
        access_token = login_response.data['access']
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {access_token}')

        # WHEN
        response = self.client.get(self.url)

        # THEN
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_list_users_unauthenticated(self):
        # WHEN
        response = self.client.get(self.url)

        # THEN
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
