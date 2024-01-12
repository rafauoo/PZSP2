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


class SchoolDetailTests(TestCase):
    def setUp(self):
        self.client = APIClient()

        self.school1 = School.objects.create(
            name='School 1',
            phone_number='verylongandsecurepassword456789',
            email='school1@example.com',
            city='City 1',
            street='Street 1',
            building_number='1',
            postcode='verylongandsecurepassword45'
        )

        self.admin = create_admin('admin@example.com', 'verylongandsecurepassword')
        self.user = create_user('user@example.com', 'verylongandsecurepassword')

        self.url = reverse('school-detail', kwargs={'id': self.school1.id})

    def perform_admin_login(self):
        login_data = {'email': 'admin@example.com', 'password': 'verylongandsecurepassword'}
        login_response = perform_login(login_data)
        access_token = login_response.data['access']
        return access_token

    def perform_user_login(self):
        login_data = {'email': 'user@example.com', 'password': 'verylongandsecurepassword'}
        login_response = perform_login(login_data)
        access_token = login_response.data['access']
        return access_token

    def test_retrieve_school_as_admin(self):
        # GIVEN
        access_token = self.perform_admin_login()
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {access_token}')

        # WHEN
        response = self.client.get(self.url)

        # THEN
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        serializer = SchoolSerializer(self.school1)
        self.assertEqual(response.data, serializer.data)

    # GIVEN
    def test_update_school_as_admin(self):
        # GIVEN
        access_token = self.perform_admin_login()
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {access_token}')

        # WHEN
        updated_data = {
            'name': 'Updated School',
            'phone_number': '9876543210',
            'email': 'updatedschool@example.com',
            'city': 'Updated City',
            'street': 'Updated Street',
            'building_number': '20',
            'postcode': '54321'
        }
        response = self.client.put(self.url, updated_data, format='json')

        # THEN
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.school1.refresh_from_db()
        self.assertEqual(self.school1.name, 'Updated School')

    def test_partial_update_school_as_admin(self):
        # GIVEN
        access_token = self.perform_admin_login()
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {access_token}')

        # WHEN
        partial_update_data = {'name': 'Partial Update for School'}
        response = self.client.patch(self.url, partial_update_data, format='json')

        # THEN
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.school1.refresh_from_db()
        self.assertEqual(self.school1.name, 'Partial Update for School')

    # GIVEN
    def test_delete_school_as_admin(self):
        # GIVEN
        access_token = self.perform_admin_login()
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {access_token}')

        # WHEN
        response = self.client.delete(self.url)

        # THEN
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        with self.assertRaises(School.DoesNotExist):
            self.school1.refresh_from_db()

    def test_retrieve_school_as_user(self):
        # GIVEN
        access_token = self.perform_user_login()
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {access_token}')

        # WHEN
        response = self.client.get(self.url)

        # THEN
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_update_school_as_user(self):
        # GIVEN
        access_token = self.perform_user_login()
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {access_token}')

        # WHEN
        updated_data = {
            'name': 'Updated School as User',
            'phone_number': '9876543210',
            'email': 'updatedschooluser@example.com',
            'city': 'Updated City User',
            'street': 'Updated Street User',
            'building_number': '20',
            'postcode': '54321'
        }
        response = self.client.put(self.url, updated_data, format='json')

        # THEN
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.school1.refresh_from_db()
        self.assertNotEqual(self.school1.name, 'Updated School as User')

    def test_partial_update_school_as_user(self):
        # GIVEN
        access_token = self.perform_user_login()
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {access_token}')

        # WHEN
        partial_update_data = {'name': 'Partial Update for School as User'}
        response = self.client.patch(self.url, partial_update_data, format='json')

        # THEN
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.school1.refresh_from_db()
        self.assertNotEqual(self.school1.name, 'Partial Update for School as User')

    def test_delete_school_as_user(self):
        # GIVEN
        access_token = self.perform_user_login()
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {access_token}')

        # WHEN
        response = self.client.delete(self.url)

        # THEN
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertTrue(School.objects.filter(id=self.school1.id).exists())

    def test_retrieve_school_unauthenticated(self):
        # WHEN
        response = self.client.get(self.url)

        # THEN
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_update_school_unauthenticated(self):
        # WHEN
        updated_data = {'name': 'Updated School'}
        response = self.client.put(self.url, updated_data, format='json')

        # THEN
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        self.school1.refresh_from_db()
        self.assertNotEqual(self.school1.name, 'Updated School')

    def test_partial_update_school_unauthenticated(self):
        # WHEN
        partial_update_data = {'name': 'Partial Update for School'}
        response = self.client.patch(self.url, partial_update_data, format='json')

        # THEN
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        self.school1.refresh_from_db()
        self.assertNotEqual(self.school1.name, 'Partial Update for School')

    def test_delete_school_unauthenticated(self):
        # WHEN
        response = self.client.delete(self.url)

        # THEN
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        self.assertTrue(School.objects.filter(id=self.school1.id).exists())

    def test_retrieve_school_as_school_user(self):
        # GIVEN
        self.user.school = self.school1
        self.user.save()

        access_token = self.perform_user_login()
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {access_token}')

        # WHEN
        response = self.client.get(self.url)

        # THEN
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        serializer = SchoolSerializer(self.school1)
        self.assertEqual(response.data, serializer.data)

    def test_update_school_as_school_user(self):
        # GIVEN
        self.user.school = self.school1
        self.user.save()

        access_token = self.perform_user_login()
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {access_token}')

        # WHEN
        updated_data = {
            'name': 'Updated School as School User',
            'phone_number': '9876543210',
            'email': 'updatedschooluser@example.com',
            'city': 'Updated City User',
            'street': 'Updated Street User',
            'building_number': '20',
            'postcode': '54321'
        }
        response = self.client.put(self.url, updated_data, format='json')

        # THEN
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.school1.refresh_from_db()
        self.assertEqual(self.school1.name, 'Updated School as School User')

    def test_partial_update_school_as_school_user(self):
        # GIVEN
        self.user.school = self.school1
        self.user.save()

        access_token = self.perform_user_login()
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {access_token}')

        # WHEN
        partial_update_data = {'name': 'Partial Update for School as School User'}
        response = self.client.patch(self.url, partial_update_data, format='json')

        # THEN
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.school1.refresh_from_db()
        self.assertEqual(self.school1.name, 'Partial Update for School as School User')

    def test_delete_school_as_school_user(self):
        # GIVEN
        self.user.school = self.school1
        self.user.save()

        access_token = self.perform_user_login()
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {access_token}')

        # WHEN
        response = self.client.delete(self.url)

        # THEN
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)  # Oczekiwany brak uprawnień
        self.assertTrue(School.objects.filter(id=self.school1.id).exists())
