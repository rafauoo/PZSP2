from django.test import TestCase
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient
from api.models import User, School
from api.serializers.user import UserSerializer

from tests.setup import create_admin, create_user
from tests.utils import perform_login


class UserDetailTests(TestCase):
    def setUp(self):
        self.client = APIClient()

        # Create an admin user
        self.admin = create_admin('admin@example.com', 'verylongandsecurepassword')

        # Create a regular user
        self.user = create_user('user@example.com', 'verylongandsecurepassword')

        # Create URLs for user details
        self.admin_url = reverse('user-detail', kwargs={'id': self.admin.id})
        self.user_url = reverse('user-detail', kwargs={'id': self.user.id})

        self.school_data = {
            'name': 'Test School',
            'phone_number': 'verylongandsecurepassword456789',
            'fax_number': '987654321',
            'email': 'school@example.com',
            'website': 'http://www.testschool.com',
            'city': 'Test City',
            'street': 'Test Street',
            'building_number': 'verylongandsecurepassword',
            'apartment_number': '45',
            'postcode': 'verylongandsecurepassword45',
        }
        self.school = School.objects.create(**self.school_data)

    def test_get_user_details_as_admin(self):
        # GIVEN
        login_data = {'email': 'admin@example.com', 'password': 'verylongandsecurepassword'}
        login_response = perform_login(login_data)
        access_token = login_response.data['access']
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {access_token}')

        # WHEN
        response = self.client.get(self.user_url)

        # THEN
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        serializer = UserSerializer(self.user)
        self.assertEqual(response.data, serializer.data)

    def test_get_user_details_as_regular_user(self):
        # GIVEN
        login_data = {'email': 'user@example.com', 'password': 'verylongandsecurepassword'}
        login_response = perform_login(login_data)
        access_token = login_response.data['access']
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {access_token}')
        # WHEN
        response = self.client.get(self.user_url)

        # THEN
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        serializer = UserSerializer(self.user)
        self.assertEqual(response.data, serializer.data)

    def test_get_user_details_unauthenticated(self):
        # WHEN
        response = self.client.get(self.user_url)

        # THEN
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_update_user_details_as_admin(self):
        # GIVEN
        login_data = {'email': 'admin@example.com', 'password': 'verylongandsecurepassword'}
        login_response = perform_login(login_data)
        access_token = login_response.data['access']
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {access_token}')

        # WHEN
        data = {
            'email': 'updated_user@example.com',
            'first_name': 'Updated First Name',
            'last_name': 'Updated Last Name',
            'school': None,  # Replace with the actual ID of the school
            'user_type': 'user',  # Replace with the actual ID of the group
            # Add more fields as needed
        }
        response = self.client.put(self.user_url, data, format='json')

        # THEN
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        updated_user = User.objects.get(id=self.user.id)
        self.assertEqual(updated_user.email, 'updated_user@example.com')

    def test_update_user_details_as_regular_user(self):
        # GIVEN
        login_data = {'email': 'user@example.com', 'password': 'verylongandsecurepassword'}
        login_response = perform_login(login_data)
        access_token = login_response.data['access']
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {access_token}')

        # WHEN
        data = {'email': 'updated_user@example.com'}
        response = self.client.put(self.user_url, data, format='json')

        # THEN
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        updated_user = User.objects.get(id=self.user.id)
        self.assertEqual(updated_user.email, 'user@example.com')

    def test_update_user_details_unauthenticated(self):
        # WHEN
        data = {'email': 'updated_user@example.com'}
        response = self.client.put(self.user_url, data, format='json')

        # THEN
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_partial_update_user_details_as_admin(self):
        # GIVEN
        login_data = {'email': 'admin@example.com', 'password': 'verylongandsecurepassword'}
        login_response = perform_login(login_data)
        access_token = login_response.data['access']
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {access_token}')

        # WHEN
        data = {'email': 'updated_user@example.com'}
        response = self.client.patch(self.user_url, data, format='json')

        # THEN
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        updated_user = User.objects.get(id=self.user.id)
        self.assertEqual(updated_user.email, 'updated_user@example.com')

    def test_partial_update_user_details_as_regular_user(self):
        # GIVEN
        login_data = {'email': 'user@example.com', 'password': 'verylongandsecurepassword'}
        login_response = perform_login(login_data)
        access_token = login_response.data['access']
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {access_token}')

        # WHEN
        data = {'email': 'updated_user@example.com'}
        response = self.client.patch(self.user_url, data, format='json')

        # THEN
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        updated_user = User.objects.get(id=self.user.id)
        self.assertEqual(updated_user.email, 'updated_user@example.com')

    def test_partial_update_user_details_unauthenticated(self):
        # WHEN
        data = {'email': 'updated_user@example.com'}
        response = self.client.patch(self.user_url, data, format='json')

        # THEN
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_delete_user_as_admin(self):
        # GIVEN
        login_data = {'email': 'admin@example.com', 'password': 'verylongandsecurepassword'}
        login_response = perform_login(login_data)
        access_token = login_response.data['access']
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {access_token}')

        # WHEN
        response = self.client.delete(self.user_url)

        # THEN
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        with self.assertRaises(User.DoesNotExist):
            User.objects.get(id=self.user.id)

    def test_delete_user_as_regular_user(self):
        # GIVEN
        login_data = {'email': 'user@example.com', 'password': 'verylongandsecurepassword'}
        login_response = perform_login(login_data)
        access_token = login_response.data['access']
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {access_token}')

        # WHEN
        response = self.client.delete(self.user_url)

        # THEN
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertIsNotNone(User.objects.get(id=self.user.id))

    def test_delete_user_unauthenticated(self):
        # WHEN
        response = self.client.delete(self.user_url)

        # THEN
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        self.assertIsNotNone(User.objects.get(id=self.user.id))
