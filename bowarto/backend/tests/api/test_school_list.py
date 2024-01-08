from django.test import TestCase
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient
from rest_framework_simplejwt.tokens import AccessToken
from api.models import School
from api.serializers.school import SchoolSerializer
from api.views.school import SchoolList, SchoolDetail
from tests.setup import create_admin, create_user
from tests.utils import perform_login


class SchoolListTests(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.url = reverse('school-list')

        self.school1 = School.objects.create(
            name='School 1',
            phone_number='123456789',
            email='school1@example.com',
            city='City 1',
            street='Street 1',
            building_number='1',
            postcode='12345'
        )
        self.school2 = School.objects.create(
            name='School 2',
            phone_number='987654321',
            email='school2@example.com',
            city='City 2',
            street='Street 2',
            building_number='2',
            postcode='54321'
        )

        self.admin = create_admin('admin@example.com', '123')
        self.user = create_user('user@example.com', '123')

    def perform_admin_login(self):
        login_data = {'email': 'admin@example.com', 'password': '123'}
        login_response = perform_login(login_data)
        access_token = login_response.data['access']
        return access_token

    def perform_user_login(self):
        login_data = {'email': 'user@example.com', 'password': '123'}
        login_response = perform_login(login_data)
        access_token = login_response.data['access']
        return access_token

    def test_list_schools_as_admin(self):
        # GIVEN
        access_token = self.perform_admin_login()
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {access_token}')

        # WHEN
        response = self.client.get(self.url)

        # THEN
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        serializer = SchoolSerializer(School.objects.all(), many=True)
        self.assertEqual(response.data, serializer.data)

    def test_create_school_as_admin(self):
        # GIVEN
        access_token = self.perform_admin_login()
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {access_token}')

        # WHEN
        data = {
            'name': 'New School',
            'phone_number': '9876543210',
            'email': 'newschool@example.com',
            'city': 'New City',
            'street': 'New Street',
            'building_number': '10',
            'postcode': '54321'
        }
        response = self.client.post(self.url, data, format='json')

        # THEN
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(School.objects.count(), 3)

    def test_list_schools_as_user(self):
        # GIVEN
        access_token = self.perform_user_login()
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {access_token}')

        # WHEN
        response = self.client.get(self.url)

        # THEN
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_create_school_as_user(self):
        # GIVEN
        access_token = self.perform_user_login()
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {access_token}')

        # WHEN
        data = {
            'name': 'New School as User',
            'phone_number': '9876543210',
            'email': 'newschooluser@example.com',
            'city': 'New City User',
            'street': 'New Street User',
            'building_number': '10',
            'postcode': '54321'
        }
        response = self.client.post(self.url, data, format='json')

        # THEN
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertEqual(School.objects.count(), 2)

    def test_list_schools_unauthenticated(self):
        # WHEN
        response = self.client.get(self.url)

        # THEN
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_create_school_unauthenticated(self):
        # WHEN
        data = {
            'name': 'New School',
            'phone_number': '9876543210',
            'email': 'newschool@example.com',
            'city': 'New City',
            'street': 'New Street',
            'building_number': '10',
            'postcode': '54321'
        }
        response = self.client.post(self.url, data, format='json')

        # THEN
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        self.assertEqual(School.objects.count(), 2)
