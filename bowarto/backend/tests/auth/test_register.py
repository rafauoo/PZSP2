from django.test import TestCase
from rest_framework import status
from rest_framework.test import APIRequestFactory
from rest_framework_simplejwt.tokens import RefreshToken
from api.models import User, School
from api.serializers.user import UserRegistrationSerializer
from api.views.auth import RegisterView
from rest_framework_simplejwt.tokens import RefreshToken, OutstandingToken, BlacklistedToken
from tests.utils import perform_register


class RegisterViewTest(TestCase):
    def setUp(self):
        self.factory = APIRequestFactory()
        self.register_url = '/path/to/register/'
        self.school_data = {
            'name': 'Test School',
            'phone_number': '123456789',
            'fax_number': '987654321',
            'email': 'school@example.com',
            'website': 'http://www.testschool.com',
            'city': 'Test City',
            'street': 'Test Street',
            'building_number': '123',
            'apartment_number': '45',
            'postcode': '12345',
        }
        self.school = School.objects.create(**self.school_data)
        self.valid_user_data = {
            'email': 'test@example.com',
            'password': 'testpassword',
            'first_name': 'first',
            'last_name': 'last',
            'school': self.school.id
        }

    def test_register_user(self):
        # GIVEN
        data = self.valid_user_data

        # WHEN
        response = perform_register(data)

        # THEN
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertIn('refresh', response.data)
        self.assertIn('access', response.data)

        user = User.objects.get(email='test@example.com')
        self.assertIsNotNone(user)

    def test_register_invalid_email(self):
        # GIVEN
        data = self.valid_user_data
        data['email'] = 'invalid_format'

        # WHEN
        response = perform_register(data)

        # THEN
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        users_with_invalid_email = User.objects.filter(email='invalid_format')
        self.assertQuerysetEqual(users_with_invalid_email, [])

    def test_register_no_school(self):
        # GIVEN
        data = self.valid_user_data
        data.pop('school')

        # WHEN
        response = perform_register(data)
        # THEN

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        user = User.objects.get(email='test@example.com')
        self.assertIsNone(user.school)

    def test_register_no_password(self):
        # GIVEN
        data = self.valid_user_data
        data.pop('password')

        # WHEN
        response = perform_register(data)

        # THEN
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        user = User.objects.filter(email='test@example.com')
        self.assertQuerysetEqual(user, [])

    def test_register_not_existing_school(self):
        # GIVEN
        data = self.valid_user_data
        data['school'] = 150

        # WHEN
        response = perform_register(data)

        # THEN
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        users_with_invalid_school = User.objects.filter(email='test@example.com')
        self.assertQuerysetEqual(users_with_invalid_school, [])

    def test_register_duplicate_email(self):
        # GIVEN
        data = self.valid_user_data

        # WHEN
        first_user_response = perform_register(data)
        second_user_response = perform_register(data)

        # THEN
        self.assertEqual(first_user_response.status_code, status.HTTP_201_CREATED)

        self.assertEqual(second_user_response.status_code, status.HTTP_400_BAD_REQUEST)
        users_with_duplicate_email = User.objects.filter(email='test@example.com')
        self.assertEqual(users_with_duplicate_email.count(), 1)

    def test_register_missing_name_or_lastname(self):
        # GIVEN
        data_missing_name = self.valid_user_data
        data_missing_name.pop('first_name')

        data_missing_lastname = self.valid_user_data
        data_missing_lastname.pop('last_name')

        # WHEN
        response_missing_name = perform_register(data_missing_name)
        response_missing_lastname = perform_register(data_missing_lastname)

        # THEN
        self.assertEqual(response_missing_name.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response_missing_lastname.status_code, status.HTTP_400_BAD_REQUEST)

        users_missing_name = User.objects.filter(email='test@example.com')
        users_missing_lastname = User.objects.filter(email='test@example.com')

        self.assertQuerysetEqual(users_missing_name, [])
        self.assertQuerysetEqual(users_missing_lastname, [])
