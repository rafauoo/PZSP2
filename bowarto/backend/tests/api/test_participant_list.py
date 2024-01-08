from django.test import TestCase
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient
from api.models import Application, User, Competition, Participant
from api.serializers.participant import ParticipantSerializer

from tests.setup import create_admin, create_user
from tests.utils import perform_login


class ParticipantListTests(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.url = reverse('participant-list')

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

    def test_list_participants_as_admin(self):
        # GIVEN
        login_data = {'email': 'admin@example.com', 'password': '123'}
        login_response = perform_login(login_data)
        access_token = login_response.data['access']
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {access_token}')

        # WHEN
        response = self.client.get(self.url)

        # THEN
        participants = Participant.objects.all()
        serializer = ParticipantSerializer(participants, many=True)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, serializer.data)

    def test_list_participants_as_user(self):
        # GIVEN
        login_data = {'email': 'user_1@example.com', 'password': '123'}
        login_response = perform_login(login_data)
        access_token = login_response.data['access']
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {access_token}')

        # WHEN
        response = self.client.get(self.url)

        # THEN
        user_participants = Participant.objects.filter(application__user=self.user_1)
        serializer = ParticipantSerializer(user_participants, many=True)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, serializer.data)

    def test_list_participants_unauthenticated(self):
        # WHEN
        response = self.client.get(self.url)

        # THEN
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_create_participant_as_user(self):
        # GIVEN
        login_data = {'email': 'user_1@example.com', 'password': '123'}
        login_response = perform_login(login_data)
        access_token = login_response.data['access']
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {access_token}')

        # WHEN
        data = {
            'application': self.application.id,
            'first_name': 'Jan',
            'last_name': 'Kowalski',
            'email': 'jan@example.com'
        }
        response = self.client.post(self.url, data, format='json')

        # THEN
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Participant.objects.count(), 2)
        participants = Participant.objects.filter(application=self.application)
        self.assertEqual(participants.last().application.user, self.user_1)

    def test_create_participant_as_admin(self):
        # GIVEN
        login_data = {'email': 'admin@example.com', 'password': '123'}
        login_response = perform_login(login_data)
        access_token = login_response.data['access']
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {access_token}')

        # WHEN
        data = {
            'application': self.application.id,
            'first_name': 'Jan',
            'last_name': 'Kowalski',
            'email': 'jan@example.com'
        }

        response = self.client.post(self.url, data, format='json')

        # THEN
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Participant.objects.count(), 2)
        participants = Participant.objects.filter(application=self.application)
        self.assertEqual(participants.last().application.user, self.user_1)

    def test_create_participant_unauthenticated(self):
        # WHEN
        data = {
            'application': self.application.id,
        }

        response = self.client.post(self.url, data, format='json')

        # THEN
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_create_participant_not_existing_application(self):
        # GIVEN
        login_data = {'email': 'user_1@example.com', 'password': '123'}
        login_response = perform_login(login_data)
        access_token = login_response.data['access']
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {access_token}')

        # WHEN
        data = {
            'application': 2137,
        }

        response = self.client.post(self.url, data, format='json')

        # THEN
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        self.assertEqual(Participant.objects.count(), 1)
