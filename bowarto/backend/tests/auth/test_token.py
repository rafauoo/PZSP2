from django.test import TestCase
from rest_framework import status
from rest_framework.test import APIRequestFactory
from rest_framework_simplejwt.tokens import RefreshToken
from api.models import User, School
from api.serializers.user import UserRegistrationSerializer
from api.views.auth import RegisterView
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework_simplejwt.tokens import RefreshToken, OutstandingToken, BlacklistedToken
from tests.utils import perform_register, perform_login, perform_logout, perform_refresh


class TestToken(TestCase):
    def setUp(self):
        self.factory = APIRequestFactory()
        self.register_data = {
            'email': 'test@example.com',
            'password': 'verylongandsecurepassword',
            'first_name': 'first',
            'last_name': 'last',
        }
        self.login_data = {
            'email': 'test@example.com',
            'password': 'verylongandsecurepassword'
        }
        perform_register(self.register_data)
        self.user = User.objects.get(email='test@example.com')

    def test_login_successful(self):
        # GIVEN
        login_data = self.login_data

        # WHEN
        response = perform_login(login_data)

        # THEN
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('access', response.data)
        self.assertIn('refresh', response.data)

    def test_login_invalid_password(self):
        # GIVEN
        login_data = self.login_data
        login_data['password'] = 'invalid_password'

        # WHEN
        response = perform_login(login_data)

        # THEN
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        self.assertNotIn('access', response.data)
        self.assertNotIn('refresh', response.data)

    def test_login_nonexistent_user(self):
        # GIVEN
        login_data = self.login_data
        login_data['email'] = 'notexistent@example.com'

        # WHEN
        response = perform_login(login_data)

        # THEN
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        self.assertNotIn('access', response.data)
        self.assertNotIn('refresh', response.data)

    def test_login_missing_credentials(self):
        # GIVEN
        login_data = {}

        # WHEN
        response = perform_login(login_data)

        # THEN
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertNotIn('access', response.data)
        self.assertNotIn('refresh', response.data)

    def test_logout_successful(self):
        # GIVEN
        login_response = perform_login(self.login_data)
        refresh_token = login_response.data['refresh']

        # WHEN
        response = perform_logout(refresh_token)

        # THEN
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        self.assertTrue(BlacklistedToken.objects.filter(token__token=refresh_token).exists())

    def test_logout_invalid_refresh_token(self):
        # GIVEN
        login_response = perform_login(self.login_data)
        refresh_token = login_response.data['refresh'] + '123'

        # WHEN
        response = perform_logout(refresh_token)

        # THEN
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

        self.assertFalse(BlacklistedToken.objects.filter(token__token=refresh_token).exists())

    def test_refresh_successful(self):
        # GIVEN
        login_response = perform_login(self.login_data)
        refresh_token = login_response.data['refresh']
        access_old = login_response.data['access']

        # WHEN
        response = perform_refresh(refresh_token)

        # THEN
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('access', response.data)
        self.assertNotEqual(access_old, response.data['access'])

    def test_refresh_blacklisted_token(self):
        # GIVEN
        login_response = perform_login(self.login_data)
        refresh_token = login_response.data['refresh']
        perform_logout(refresh_token)

        # WHEN
        response = perform_refresh(refresh_token)

        # THEN
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
