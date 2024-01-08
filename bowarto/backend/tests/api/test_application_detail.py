from django.test import TestCase
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient
from api.models import Application, User, Competition
from api.serializers.application import ApplicationSerializer

from tests.setup import create_admin, create_user
from tests.utils import perform_login


class ApplicationDetailTests(TestCase):
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

        self.url = reverse('application-detail', kwargs={'id': self.application.id})

    def test_get_application_as_admin(self):
        # GIVEN
        login_data = {'email': 'admin@example.com', 'password': '123'}
        login_response = perform_login(login_data)
        access_token = login_response.data['access']
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {access_token}')

        # WHEN
        response = self.client.get(self.url)

        # THEN
        serializer = ApplicationSerializer(self.application)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, serializer.data)

    def test_get_application_as_user(self):
        # GIVEN
        login_data = {'email': 'user_1@example.com', 'password': '123'}
        login_response = perform_login(login_data)
        access_token = login_response.data['access']
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {access_token}')

        # WHEN
        response = self.client.get(self.url)

        # THEN
        serializer = ApplicationSerializer(self.application)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, serializer.data)

    def test_get_application_unauthenticated(self):
        # WHEN
        response = self.client.get(self.url)

        # THEN
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_delete_application_as_admin(self):
        # GIVEN
        login_data = {'email': 'admin@example.com', 'password': '123'}
        login_response = perform_login(login_data)
        access_token = login_response.data['access']
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {access_token}')

        # WHEN
        response = self.client.delete(self.url)

        # THEN
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Application.objects.count(), 0)

    def test_delete_application_as_user(self):
        # GIVEN
        login_data = {'email': 'user_1@example.com', 'password': '123'}
        login_response = perform_login(login_data)
        access_token = login_response.data['access']
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {access_token}')

        # WHEN
        response = self.client.delete(self.url)

        # THEN
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Application.objects.count(), 0)

    def test_delete_application_as_user_other_user_application(self):
        # GIVEN
        login_data = {'email': 'user_2@example.com', 'password': '123'}
        login_response = perform_login(login_data)
        access_token = login_response.data['access']
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {access_token}')

        # WHEN
        response = self.client.delete(self.url)

        # THEN
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertEqual(Application.objects.count(), 1)

    def test_delete_application_unauthenticated(self):
        # WHEN
        response = self.client.delete(self.url)

        # THEN
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
