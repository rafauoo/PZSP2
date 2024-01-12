from django.test import TestCase
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient
from api.models import Competition, User
from api.serializers.competition import CompetitionSerializer
from datetime import datetime, timedelta

from tests.setup import create_admin, create_user
from tests.utils import perform_login


class CompetitionDetailTests(TestCase):
    def setUp(self):
        self.client = APIClient()

        # Utwórz konkurs do testowania
        self.competition = Competition.objects.create(
            title='Test Competition',
            description='Description for Test Competition',
            start_at=datetime.now(),
            end_at=datetime.now() + timedelta(days=7)
        )

        # Utwórz użytkownika do testowania
        self.user = create_user('user@example.com', 'verylongandsecurepassword')
        self.admin = create_admin('admin@example.com', 'verylongandsecurepassword')
        # Ustaw URL dla widoku CompetitionDetail z użyciem id utworzonego konkursu
        self.url = reverse('competition-detail', kwargs={'id': self.competition.id})

    def perform_user_login(self):
        login_data = {'email': 'user@example.com', 'password': 'verylongandsecurepassword'}
        login_response = perform_login(login_data)
        return login_response.data['access']

    def perform_admin_login(self):
        login_data = {'email': 'admin@example.com', 'password': 'verylongandsecurepassword'}
        login_response = perform_login(login_data)
        return login_response.data['access']

    def test_retrieve_competition(self):
        # WHEN
        response = self.client.get(self.url)

        # THEN
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        serializer = CompetitionSerializer(self.competition)
        self.assertEqual(response.data, serializer.data)

    def test_partial_update_competition_as_admin(self):
        # GIVEN
        access_token = self.perform_admin_login()
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {access_token}')

        # WHEN
        partial_update_data = {
            'title': 'Partial Update for Test Competition'
        }

        response = self.client.patch(self.url, partial_update_data, format='json')

        # THEN
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.competition.refresh_from_db()
        self.assertEqual(self.competition.title, 'Partial Update for Test Competition')

    def test_delete_competition_as_admin(self):
        # GIVEN
        access_token = self.perform_admin_login()
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {access_token}')

        # WHEN
        response = self.client.delete(self.url)

        # THEN
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        with self.assertRaises(Competition.DoesNotExist):
            self.competition.refresh_from_db()

    def test_retrieve_competition_unauthenticated(self):
        # GIVEN

        # WHEN
        response = self.client.get(self.url)

        # THEN
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        serializer = CompetitionSerializer(self.competition)
        self.assertEqual(response.data, serializer.data)

    def test_update_competition_unauthenticated(self):
        # GIVEN

        # WHEN
        updated_data = {
            'title': 'Updated Test Competition',
            'description': 'Updated Description for Test Competition',
            'start_at': datetime.now().isoformat(),
            'end_at': (datetime.now() + timedelta(days=14)).isoformat()
        }

        response = self.client.put(self.url, updated_data, format='json')

        # THEN
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_update_competition_as_user(self):
        # GIVEN
        access_token = self.perform_user_login()
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {access_token}')

        # WHEN
        updated_data = {
            'title': 'Updated Test Competition',
            'description': 'Updated Description for Test Competition',
            'start_at': datetime.now().isoformat(),
            'end_at': (datetime.now() + timedelta(days=14)).isoformat()
        }

        response = self.client.put(self.url, updated_data, format='json')

        # THEN
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_partial_update_competition_as_user(self):
        # GIVEN
        access_token = self.perform_user_login()
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {access_token}')

        # WHEN
        partial_update_data = {
            'title': 'Partial Update for Test Competition'
        }
        response = self.client.patch(self.url, partial_update_data, format='json')

        # THEN
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_delete_competition_as_user(self):
        # GIVEN
        access_token = self.perform_user_login()
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {access_token}')

        # WHEN
        response = self.client.delete(self.url)

        # THEN
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertTrue(Competition.objects.filter(id=self.competition.id).exists())
