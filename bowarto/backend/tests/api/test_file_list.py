from django.core.files.uploadedfile import SimpleUploadedFile
from django.core.files.storage import default_storage
from django.test import TestCase
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient
from unittest.mock import patch
from api.models import File, FileType, CompetitionType, User, Competition, Application, Participant
from datetime import datetime, timedelta
from tests.setup import create_admin, create_user
from tests.utils import perform_login


class FileListTests(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.url = reverse('file-list')

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

    def test_get_files_as_admin(self):
        # GIVEN
        login_data = {'email': 'admin@example.com', 'password': '123'}
        login_response = perform_login(login_data)
        access_token = login_response.data['access']
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {access_token}')

        # WHEN
        response = self.client.get(self.url)

        # THEN
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), File.objects.count())

    def test_get_files_as_user(self):
        # GIVEN
        login_data = {'email': 'user_1@example.com', 'password': '123'}
        login_response = perform_login(login_data)
        access_token = login_response.data['access']
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {access_token}')

        # WHEN
        response = self.client.get(self.url)

        # THEN
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data),
                         File.objects.filter(participant__application__user=self.user_1).count())

    def test_get_files_unauthenticated(self):
        # WHEN
        response = self.client.get(self.url)

        # THEN
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_create_file_by_admin(self):
        # GIVEN
        login_data = {'email': 'admin@example.com', 'password': '123'}
        login_response = perform_login(login_data)
        access_token = login_response.data['access']
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {access_token}')

        with patch('api.views.file.is_allowed_file_type') as mock_is_allowed_file_type:
            try:
                # WHEN
                mock_is_allowed_file_type.return_value = True
                file_content = b'Test file content'
                uploaded_file = SimpleUploadedFile("test_file.pdf", file_content, content_type="application/pdf")
                file_data = {
                    'path': uploaded_file,
                    'competition': self.competition.id,
                    'type': self.file_type_2.id,
                    # 'participant': self.participant_1_app_1.id
                }
                response = self.client.post(self.url, data=file_data, format='multipart')

                # THEN
                self.assertEqual(response.status_code, status.HTTP_201_CREATED)
                self.assertEqual(File.objects.filter(type=self.file_type_2).count(), 1)

                file = File.objects.get(type=self.file_type_2)
                self.assertEqual(file.type.name, "regulamin")
                self.assertTrue(default_storage.exists(file.path.name))
            finally:
                self.tearDown()

    def test_create_file_by_user(self):
        # GIVEN
        login_data = {'email': 'user_1@example.com', 'password': '123'}
        login_response = perform_login(login_data)
        access_token = login_response.data['access']
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {access_token}')

        with patch('api.views.file.is_allowed_file_type') as mock_is_allowed_file_type:
            try:
                # WHEN
                mock_is_allowed_file_type.return_value = True
                file_content = b'Test file content'
                uploaded_file = SimpleUploadedFile("test_file.pdf", file_content, content_type="application/pdf")
                file_data = {
                    'path': uploaded_file,
                    # 'competition': self.competition.id,
                    # 'type': self.file_type_1.id,
                    'participant': self.participant_1_app_1.id
                }
                response = self.client.post(self.url, data=file_data, format='multipart')

                # THEN
                self.assertEqual(response.status_code, status.HTTP_201_CREATED)
                self.assertEqual(File.objects.filter(type=self.file_type_1).count(), 1)

                file = File.objects.get(type=self.file_type_1)
                self.assertEqual(file.type.name, "praca konkursowa")
                self.assertTrue(default_storage.exists(file.path.name))
            finally:
                self.tearDown()

    def test_create_file_by_user_to_others_user_participant(self):
        # GIVEN
        login_data = {'email': 'user_1@example.com', 'password': '123'}
        login_response = perform_login(login_data)
        access_token = login_response.data['access']
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {access_token}')

        with patch('api.views.file.is_allowed_file_type') as mock_is_allowed_file_type:
            try:
                # WHEN
                mock_is_allowed_file_type.return_value = True
                file_content = b'Test file content'
                uploaded_file = SimpleUploadedFile("test_file.pdf", file_content, content_type="application/pdf")
                file_data = {
                    'path': uploaded_file,
                    # 'competition': self.competition.id,
                    # 'type': self.file_type_1.id,
                    'participant': self.participant_1_app_2.id
                }
                response = self.client.post(self.url, data=file_data, format='multipart')

                # THEN
                self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
                self.assertEqual(File.objects.filter(type=self.file_type_1).count(), 0)

            finally:
                self.tearDown()

    def test_create_competition_file_by_user(self):
        # GIVEN
        login_data = {'email': 'user_1@example.com', 'password': '123'}
        login_response = perform_login(login_data)
        access_token = login_response.data['access']
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {access_token}')

        with patch('api.views.file.is_allowed_file_type') as mock_is_allowed_file_type:
            try:
                # WHEN
                mock_is_allowed_file_type.return_value = True
                file_content = b'Test file content'
                uploaded_file = SimpleUploadedFile("test_file.pdf", file_content, content_type="application/pdf")
                file_data = {
                    'path': uploaded_file,
                    'competition': self.competition.id,
                    'type': self.file_type_2.id,
                }
                response = self.client.post(self.url, data=file_data, format='multipart')

                # THEN
                self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
                self.assertEqual(File.objects.filter(type=self.file_type_2).count(), 0)
            finally:
                self.tearDown()

    def test_create_competition_file_by_user_both_competition_and_participant_set(self):
        # GIVEN
        login_data = {'email': 'user_1@example.com', 'password': '123'}
        login_response = perform_login(login_data)
        access_token = login_response.data['access']
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {access_token}')

        with patch('api.views.file.is_allowed_file_type') as mock_is_allowed_file_type:
            try:
                # WHEN
                mock_is_allowed_file_type.return_value = True
                file_content = b'Test file content'
                uploaded_file = SimpleUploadedFile("test_file.pdf", file_content, content_type="application/pdf")
                file_data = {
                    'path': uploaded_file,
                    'competition': self.competition.id,
                    'type': self.file_type_2.id,
                    'participant': self.participant_1_app_1.id,
                }
                response = self.client.post(self.url, data=file_data, format='multipart')

                # THEN
                self.assertEqual(response.status_code, status.HTTP_201_CREATED)

                self.assertEqual(File.objects.filter(type=self.file_type_2).count(), 0)
                self.assertEqual(File.objects.filter(competition=self.competition).count(), 0)

                self.assertEqual(File.objects.filter(type=self.file_type_1).count(), 1)
                self.assertEqual(File.objects.filter(participant=self.participant_1_app_1).count(), 1)

                file = File.objects.get(type=self.file_type_1)
                self.assertIsNone(file.competition)
                self.assertEqual(file.type, self.file_type_1)
            finally:
                self.tearDown()

    def test_create_file_with_wrong_type(self):
        # GIVEN
        login_data = {'email': 'admin@example.com', 'password': '123'}
        login_response = perform_login(login_data)
        access_token = login_response.data['access']
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {access_token}')
        try:
            # WHEN
            file_content = b'Test file content'
            uploaded_file = SimpleUploadedFile("test_file.pdf", file_content, content_type="application/pdf")
            file_data = {
                'path': uploaded_file,
                'competition': self.competition.id,
                'type': self.file_type_2.id,
                # 'participant': self.participant_1_app_1.id
            }
            response = self.client.post(self.url, data=file_data, format='multipart')

            # THEN
            self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
            self.assertEqual(File.objects.filter(type=self.file_type_2).count(), 0)

        finally:
            self.tearDown()

    def tearDown(self):
        for file in File.objects.all():
            file.delete()
