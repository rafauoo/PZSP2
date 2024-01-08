from django.test import TestCase
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient
from unittest.mock import patch
from django.core.files.uploadedfile import SimpleUploadedFile
from django.core.files.storage import default_storage

from datetime import datetime, timedelta
from api.models import File, FileType, Competition, Application, Participant
from tests.setup import create_admin, create_user
from tests.utils import perform_login


class FileDetailTests(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.admin = create_admin('admin@example.com', '123')
        self.user_1 = create_user('user_1@example.com', '123')
        self.user_2 = create_user('user_2@example.com', '123')

        self.file_type_1 = FileType.objects.create(name='praca konkursowa')
        self.file_type_2 = FileType.objects.create(name='regulamin')

        self.competition = Competition.objects.create(
            title='Test Competition 1',
            description='Description for Competition 1',
            created_at=datetime.now(),
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

        self.participant_file = File.objects.create(
            type=self.file_type_1,
            participant=self.participant_1_app_1,
            path=SimpleUploadedFile("test_file.txt", b"file_content"),
        )

        self.competition_file = File.objects.create(
            type=self.file_type_2,
            competition=self.competition,
            path=SimpleUploadedFile("test_file.txt", b"file_content"),
        )
        self.participant_file_url = reverse('file-detail', kwargs={'id': self.participant_file.id})
        self.competition_file_url = reverse('file-detail', kwargs={'id': self.competition_file.id})

    def test_get_file_by_id_admin(self):
        # GIVEN
        login_data = {'email': 'admin@example.com', 'password': '123'}
        login_response = perform_login(login_data)
        access_token = login_response.data['access']
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {access_token}')

        # WHEN
        response = self.client.get(self.competition_file_url)

        # THEN
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue(default_storage.exists(self.competition_file.path.name))

        # CLEANUP
        self.tearDown()

    def test_get_admin_file_by_user(self):
        # GIVEN
        login_data = {'email': 'user_1@example.com', 'password': '123'}
        login_response = perform_login(login_data)
        access_token = login_response.data['access']
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {access_token}')

        # WHEN
        response = self.client.get(self.competition_file_url)

        # THEN
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

        # CLEANUP
        self.tearDown()

    def test_get_file_by_id_user(self):
        # GIVEN
        login_data = {'email': 'user_1@example.com', 'password': '123'}
        login_response = perform_login(login_data)
        access_token = login_response.data['access']
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {access_token}')

        # WHEN
        response = self.client.get(self.participant_file_url)

        # THEN
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue(default_storage.exists(self.participant_file.path.name))

        # CLEANUP
        self.tearDown()

    def test_get_file_by_id_user_not_allowed(self):
        # GIVEN
        login_data = {'email': 'user_2@example.com', 'password': '123'}
        login_response = perform_login(login_data)
        access_token = login_response.data['access']
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {access_token}')

        # WHEN
        response = self.client.get(self.participant_file_url)

        # THEN
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

        # CLEANUP
        self.tearDown()

    def test_delete_file_by_id_admin(self):
        # GIVEN
        login_data = {'email': 'admin@example.com', 'password': '123'}
        login_response = perform_login(login_data)
        access_token = login_response.data['access']
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {access_token}')

        # WHEN
        response = self.client.delete(self.competition_file_url)

        # THEN
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(default_storage.exists(self.competition_file.path.name))

        # CLEANUP
        self.tearDown()

    def test_delete_admin_file_by_user(self):
        # GIVEN
        login_data = {'email': 'user_1@example.com', 'password': '123'}
        login_response = perform_login(login_data)
        access_token = login_response.data['access']
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {access_token}')

        # WHEN
        response = self.client.delete(self.competition_file_url)

        # THEN
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertTrue(default_storage.exists(self.competition_file.path.name))

        # CLEANUP
        self.tearDown()

    def test_delete_file_by_id_user(self):
        # GIVEN
        login_data = {'email': 'user_1@example.com', 'password': '123'}
        login_response = perform_login(login_data)
        access_token = login_response.data['access']
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {access_token}')

        # WHEN
        response = self.client.delete(self.participant_file_url)

        # THEN
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(default_storage.exists(self.participant_file.path.name))

        # CLEANUP
        self.tearDown()

    def test_delete_file_by_id_user_not_allowed(self):
        # GIVEN
        login_data = {'email': 'user_2@example.com', 'password': '123'}
        login_response = perform_login(login_data)
        access_token = login_response.data['access']
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {access_token}')

        # WHEN
        response = self.client.delete(self.participant_file_url)

        # THEN
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

        # CLEANUP
        self.tearDown()

    def tearDown(self):
        for file in File.objects.all():
            file.delete()
