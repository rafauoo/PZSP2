from django.test import TestCase
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient
from api.models import Application, User, Competition, Participant
from api.serializers.participant import ParticipantSerializer

from tests.setup import create_admin, create_user
from tests.utils import perform_login


class ParticipantDetailTests(TestCase):
    def setUp(self):
        self.client = APIClient()

        self.competition = Competition.objects.create(
            title='Test Competition',
            description='Description for Competition',
        )

        self.admin = create_admin('admin@example.com', '123')
        self.user_1 = create_user('user_1@example.com', '123')
        self.user_2 = create_user('user_2@example.com', '123')

        self.application = Application.objects.create(
            competition=self.competition,
            user=self.user_1,
        )

        self.participant = Participant.objects.create(
            application=self.application,
            first_name='John',
            last_name='Doe',
            email='john@example.com'
        )

        self.url = reverse('participant-detail', kwargs={'id': self.participant.id})

    def test_get_participant_as_admin(self):
        # GIVEN
        login_data = {'email': 'admin@example.com', 'password': '123'}
        login_response = perform_login(login_data)
        access_token = login_response.data['access']
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {access_token}')

        # WHEN
        response = self.client.get(self.url)

        # THEN
        serializer = ParticipantSerializer(self.participant)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, serializer.data)

    def test_get_participant_as_user(self):
        # GIVEN
        login_data = {'email': 'user_1@example.com', 'password': '123'}
        login_response = perform_login(login_data)
        access_token = login_response.data['access']
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {access_token}')

        # WHEN
        response = self.client.get(self.url)

        # THEN
        serializer = ParticipantSerializer(self.participant)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, serializer.data)

    def test_get_participant_unauthenticated(self):
        # WHEN
        response = self.client.get(self.url)

        # THEN
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_update_participant_as_user(self):
        # GIVEN
        login_data = {'email': 'user_1@example.com', 'password': '123'}
        login_response = perform_login(login_data)
        access_token = login_response.data['access']
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {access_token}')

        # WHEN
        updated_data = {
            'application': self.application.id,
            'first_name': 'UpdatedName',
            'last_name': 'UpdatedLastName',
            'email': 'updated@example.com'
        }

        response = self.client.put(self.url, updated_data, format='json')

        # THEN
        self.participant.refresh_from_db()
        serializer = ParticipantSerializer(self.participant)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, serializer.data)
        self.assertEqual(self.participant.first_name, 'UpdatedName')
        self.assertEqual(self.participant.last_name, 'UpdatedLastName')
        self.assertEqual(self.participant.email, 'updated@example.com')

    def test_update_participant_as_admin(self):
        # GIVEN
        login_data = {'email': 'admin@example.com', 'password': '123'}
        login_response = perform_login(login_data)
        access_token = login_response.data['access']
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {access_token}')

        # WHEN
        updated_data = {
            'application': self.application.id,
            'first_name': 'UpdatedName',
            'last_name': 'UpdatedLastName',
            'email': 'updated@example.com'
        }

        response = self.client.put(self.url, updated_data, format='json')

        # THEN
        self.participant.refresh_from_db()
        serializer = ParticipantSerializer(self.participant)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, serializer.data)
        self.assertEqual(self.participant.first_name, 'UpdatedName')
        self.assertEqual(self.participant.last_name, 'UpdatedLastName')
        self.assertEqual(self.participant.email, 'updated@example.com')

    def test_update_participant_unauthenticated(self):
        # WHEN
        updated_data = {
            'first_name': 'UpdatedName',
            'last_name': 'UpdatedLastName',
            'email': 'updated@example.com'
        }

        response = self.client.put(self.url, updated_data, format='json')

        # THEN
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_partial_update_participant_as_user(self):
        # GIVEN
        login_data = {'email': 'user_1@example.com', 'password': '123'}
        login_response = perform_login(login_data)
        access_token = login_response.data['access']
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {access_token}')

        # WHEN
        partial_update_data = {
            'first_name': 'UpdatedName',
        }

        response = self.client.patch(self.url, partial_update_data, format='json')

        # THEN
        self.participant.refresh_from_db()
        serializer = ParticipantSerializer(self.participant)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, serializer.data)
        self.assertEqual(self.participant.first_name, 'UpdatedName')

    def test_partial_update_participant_as_admin(self):
        # GIVEN
        login_data = {'email': 'admin@example.com', 'password': '123'}
        login_response = perform_login(login_data)
        access_token = login_response.data['access']
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {access_token}')

        # WHEN
        partial_update_data = {
            'first_name': 'UpdatedName',
        }

        response = self.client.patch(self.url, partial_update_data, format='json')

        # THEN
        self.participant.refresh_from_db()
        serializer = ParticipantSerializer(self.participant)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, serializer.data)
        self.assertEqual(self.participant.first_name, 'UpdatedName')

    def test_partial_update_participant_unauthenticated(self):
        # WHEN
        partial_update_data = {
            'first_name': 'UpdatedName',
        }

        response = self.client.patch(self.url, partial_update_data, format='json')

        # THEN
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_delete_participant_as_user(self):
        # GIVEN
        login_data = {'email': 'user_1@example.com', 'password': '123'}
        login_response = perform_login(login_data)
        access_token = login_response.data['access']
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {access_token}')

        # WHEN
        response = self.client.delete(self.url)

        # THEN
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Participant.objects.count(), 0)

    def test_delete_participant_as_admin(self):
        # GIVEN
        login_data = {'email': 'admin@example.com', 'password': '123'}
        login_response = perform_login(login_data)
        access_token = login_response.data['access']
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {access_token}')

        # WHEN
        response = self.client.delete(self.url)

        # THEN
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Participant.objects.count(), 0)

    def test_delete_participant_unauthenticated(self):
        # WHEN
        response = self.client.delete(self.url)

        # THEN
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
