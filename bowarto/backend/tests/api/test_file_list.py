from django.core.files.uploadedfile import SimpleUploadedFile
from django.core.files.storage import default_storage
from django.test import TestCase
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient
from unittest.mock import patch
from api.models import File, CompetitionType, User, Competition, Application, Participant
from datetime import datetime, timedelta
from tests.setup import create_admin, create_user
from tests.utils import perform_login


class FileListTests(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.url = reverse('file-list')

        self.admin = create_admin('admin@example.com', 'verylongandsecurepassword')
        self.user_1 = create_user('user_1@example.com', 'verylongandsecurepassword')
        self.user_2 = create_user('user_2@example.com', 'verylongandsecurepassword')

        self.competition = Competition.objects.create(
            title='Test Competition 1',
            description='Description for Competition 1',
            start_at=datetime.now(),
            end_at=(datetime.now() + timedelta(days=7)).isoformat()
        )

        self.application_1 = Application.objects.create(user=self.user_1, competition=self.competition)
        self.application_2 = Application.objects.create(user=self.user_2, competition=self.competition)

        self.participant_1_app_1 = Participant.objects.create(email='participant_app_1@example.com',
                                                              application=self.application_1, first_name='jan',
                                                              last_name='kowalski')
        self.participant_1_app_2 = Participant.objects.create(email='participant_1_app_2@example.com',
                                                              application=self.application_2, first_name='jan',
                                                              last_name='kowalski')

    def tearDown(self):
        for file in File.objects.all():
            file.delete()

    def test_get_files_as_admin(self):
        # GIVEN
        login_data = {'email': 'admin@example.com', 'password': 'verylongandsecurepassword'}
        login_response = perform_login(login_data)
        access_token = login_response.data['access']
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {access_token}')

        # WHEN
        response = self.client.get(self.url)

        # THEN
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), File.objects.count())

        self.tearDown()

    def test_get_files_as_user(self):
        # GIVEN
        login_data = {'email': 'user_1@example.com', 'password': 'verylongandsecurepassword'}
        login_response = perform_login(login_data)
        access_token = login_response.data['access']
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {access_token}')

        # WHEN
        response = self.client.get(self.url)

        # THEN
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data),
                         File.objects.filter(attachment_participant__application__user=self.user_1).count())

        self.tearDown()

    def test_get_files_unauthenticated(self):
        # WHEN
        response = self.client.get(self.url)

        # THEN
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

        self.tearDown()
