from collections import OrderedDict

from django.test import TestCase
from rest_framework import status
from rest_framework.test import APIRequestFactory, APIClient
from rest_framework_simplejwt.tokens import RefreshToken
from api.models import User, School
from api.serializers.user import UserRegistrationSerializer
from api.views.auth import RegisterView
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework_simplejwt.tokens import RefreshToken, OutstandingToken, BlacklistedToken
from tests.utils import perform_register, perform_login, perform_logout, perform_refresh

from tests.setup import create_user, create_admin
from django.urls import reverse


class TestProfile(TestCase):
    def setUp(self):
        self.client = APIClient()

        self.user = create_user('user@example.com', '123')
        self.admin = create_admin('admin@example.com', '123')
        self.url = reverse('me')

    def test_profile_view_user(self):
        # GIVEN
        login_data = {'email': 'user@example.com', 'password': '123'}
        login_response = perform_login(login_data)
        access_token = login_response.data['access']
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {access_token}')

        # WHEN: Send GET request to the ProfileView
        response = self.client.get(self.url)
        # THEN: Assert the response status code is 200 OK
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        # THEN: Assert the response data matches the expected user data
        expected_data = {
            'id': self.user.id,
            'email': self.user.email,
            'first_name': self.user.first_name,
            'last_name': self.user.last_name,
            'user_type': 'user'
        }

        for key, value in expected_data.items():
            self.assertEqual(response.data[key], value)

    def test_profile_view_unauthenticated(self):
        # WHEN: Send GET request to the ProfileView without authentication
        response = self.client.get(self.url, format='json')

        # THEN: Assert the response status code is 401 Unauthorized
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
