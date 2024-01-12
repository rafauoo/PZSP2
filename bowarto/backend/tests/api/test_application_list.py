from datetime import timedelta, datetime

from django.test import TestCase
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient
from api.models import Application, User, Competition
from api.serializers.application import ApplicationSerializer

from tests.setup import create_admin, create_user
from tests.utils import perform_login


class ApplicationListTests(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.url = reverse('application-list')

        self.competition = Competition.objects.create(
            title='Test Competition',
            description='Description for Competition',
            start_at=datetime.now(),
            end_at=datetime.now() + timedelta(days=7)
        )

        self.admin = create_admin('admin@example.com', 'verylongandsecurepassword')
        self.user = create_user('user@example.com', 'verylongandsecurepassword')

    def test_list_applications_as_admin(self):
        # GIVEN
        login_data = {'email': 'admin@example.com', 'password': 'verylongandsecurepassword'}
        login_response = perform_login(login_data)
        access_token = login_response.data['access']
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {access_token}')

        # WHEN
        response = self.client.get(self.url)

        # THEN
        applications = Application.objects.all()
        serializer = ApplicationSerializer(applications, many=True)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, serializer.data)

    def test_list_applications_as_user(self):
        # GIVEN
        login_data = {'email': 'user@example.com', 'password': 'verylongandsecurepassword'}
        login_response = perform_login(login_data)
        access_token = login_response.data['access']
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {access_token}')

        # WHEN
        response = self.client.get(self.url)

        # THEN
        user_applications = Application.objects.filter(user=self.user)
        serializer = ApplicationSerializer(user_applications, many=True)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, serializer.data)

    def test_list_applications_unauthenticated(self):
        # WHEN
        response = self.client.get(self.url)

        # THEN
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_create_application_as_user(self):
        # GIVEN
        login_data = {'email': 'user@example.com', 'password': 'verylongandsecurepassword'}
        login_response = perform_login(login_data)
        access_token = login_response.data['access']
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {access_token}')

        # WHEN
        data = {
            'competition': self.competition.id,
        }

        response = self.client.post(self.url, data, format='json')

        # THEN
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Application.objects.count(), 1)
        application = Application.objects.get()
        self.assertEqual(application.user, self.user)

    def test_create_application_as_admin(self):
        # GIVEN
        login_data = {'email': 'admin@example.com', 'password': 'verylongandsecurepassword'}
        login_response = perform_login(login_data)
        access_token = login_response.data['access']
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {access_token}')

        # WHEN
        data = {
            'competition': self.competition.id,
            'user': self.user.id
        }

        response = self.client.post(self.url, data, format='json')

        # THEN
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Application.objects.count(), 1)
        application = Application.objects.get()
        self.assertEqual(application.user, self.user)

    def test_create_application_unauthenticated(self):
        # WHEN
        data = {
            'competition': self.competition.id,
        }

        response = self.client.post(self.url, data, format='json')

        # THEN
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_create_application_not_existing_competition(self):
        # GIVEN
        login_data = {'email': 'user@example.com', 'password': 'verylongandsecurepassword'}
        login_response = perform_login(login_data)
        access_token = login_response.data['access']
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {access_token}')

        # WHEN
        data = {
            'competition': 2137,
        }

        response = self.client.post(self.url, data, format='json')

        # THEN
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        self.assertEqual(Application.objects.count(), 0)

    def test_create_application_empty_data(self):
        # GIVEN
        login_data = {'email': 'user@example.com', 'password': 'verylongandsecurepassword'}
        login_response = perform_login(login_data)
        access_token = login_response.data['access']
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {access_token}')

        # WHEN
        data = {}

        response = self.client.post(self.url, data, format='json')

        # THEN
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(Application.objects.count(), 0)
