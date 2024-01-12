from django.test import TestCase
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient
from api.models import Competition, User
from api.serializers.competition import CompetitionSerializer
from datetime import datetime, timedelta
from tests.setup import create_admin, create_user
from tests.utils import perform_login


class CompetitionListTests(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.url = reverse('competition-list')

        self.competition1 = Competition.objects.create(
            title='Test Competition 1',
            description='Description for Competition 1',
            start_at=datetime.now(),
            end_at=(datetime.now() + timedelta(days=7)).isoformat()
        )
        self.competition2 = Competition.objects.create(
            title='Test Competition 2',
            description='Description for Competition 2',
            start_at=datetime.now(),
            end_at=(datetime.now() + timedelta(days=14)).isoformat()
        )

        self.admin = create_admin('admin@example.com', 'verylongandsecurepassword')
        self.user = create_user('user@example.com', 'verylongandsecurepassword')

    def test_list_competitions(self):
        # GIVEN

        # WHEN
        response = self.client.get(self.url)

        # THEN
        competitions = Competition.objects.all()
        serializer = CompetitionSerializer(competitions, many=True)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, serializer.data)

    def test_create_competition_as_admin(self):
        # GIVEN
        login_data = {'email': 'admin@example.com', 'password': 'verylongandsecurepassword'}
        login_response = perform_login(login_data)
        access_token = login_response.data['access']
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {access_token}')

        # WHEN
        data = {
            'title': 'New Test Competition',
            'description': 'Description for New Competition',
            'start_at': datetime.now().isoformat(),
            'end_at': (datetime.now() + timedelta(days=30)).isoformat()
        }

        response = self.client.post(self.url, data, format='json')

        # THEN
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Competition.objects.count(), 3)

    def test_create_competition_as_non_admin(self):
        # GIVEN
        login_data = {'email': 'user@example.com', 'password': 'verylongandsecurepassword'}
        login_response = perform_login(login_data)
        access_token = login_response.data['access']
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {access_token}')

        # WHEN
        data = {
            'title': 'New Test Competition',
            'description': 'Description for New Competition',
            'start_at': datetime.now().isoformat(),
            'end_at': (datetime.now() + timedelta(days=30)).isoformat()
        }
        response = self.client.post(self.url, data, format='json')

        # THEN
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertEqual(Competition.objects.count(), 2)
