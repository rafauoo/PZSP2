from django.test import TestCase
from django.urls import reverse
from django.utils import timezone
from rest_framework.test import APIClient
from rest_framework import status
from datetime import timedelta
from django.core.files.uploadedfile import SimpleUploadedFile

from api.models import File, Participant, User, Application, Competition
from tests.setup import create_admin, create_user
from tests.utils import perform_login


class TestFileDetail(TestCase):
    def setUp(self):
        self.client = APIClient()

        self.admin = create_admin('admin@example.com',
                                  'verylongandsecurepassword')
        self.user = create_user('user@example.com', 'verylongandsecurepassword')

        self.competition = Competition.objects.create(
            title='Test Competition 1',
            description='Description for Competition 1',
            start_at=timezone.now(),
            end_at=(timezone.now() + timedelta(days=7)).isoformat(),
            poster=File.objects.create(
                path=SimpleUploadedFile("poster.png", b"file_content")),
            regulation=File.objects.create(
                path=SimpleUploadedFile("regulations.docx", b"file_content"))
        )

        self.application = Application.objects.create(
            competition=self.competition,
            user=self.user

        )
        self.participant = Participant.objects.create(
            email='participant@example.com',
            application=self.application,
            first_name='John',
            last_name='Doe',
            attachment=File.objects.create(
                path=SimpleUploadedFile("participant_file.pdf",
                                        b"file_content"))
        )

        self.participant_file_url = reverse('file-detail', kwargs={
            'id': self.participant.attachment.id})
        self.poster_url = reverse('file-detail',
                                  kwargs={'id': self.competition.poster.id})
        self.regulations_url = reverse('file-detail', kwargs={
            'id': self.competition.regulation.id})

    def tearDown(self):
        for file in File.objects.all():
            file.delete()

    def test_get_file_as_admin(self):
        # GIVEN
        login_data = {'email': 'admin@example.com',
                      'password': 'verylongandsecurepassword'}
        login_response = perform_login(login_data)
        access_token = login_response.data['access']
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {access_token}')

        # WHEN
        response_participant = self.client.get(self.participant_file_url)
        response_poster = self.client.get(self.poster_url)
        response_regulations = self.client.get(self.regulations_url)

        # THEN
        self.assertEqual(response_participant.status_code, status.HTTP_200_OK)
        self.assertEqual(response_poster.status_code, status.HTTP_200_OK)
        self.assertEqual(response_regulations.status_code, status.HTTP_200_OK)

        self.tearDown()

    def test_get_file_as_user_with_permission(self):
        # GIVEN
        login_data = {'email': 'user@example.com',
                      'password': 'verylongandsecurepassword'}
        login_response = perform_login(login_data)
        access_token = login_response.data['access']
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {access_token}')

        # WHEN
        response = self.client.get(self.participant_file_url)

        # THEN
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        self.tearDown()

    def test_get_file_as_user_without_permission(self):
        # GIVEN
        login_data = {'email': 'user@example.com',
                      'password': 'verylongandsecurepassword'}
        login_response = perform_login(login_data)
        access_token = login_response.data['access']
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {access_token}')

        # WHEN
        response_poster = self.client.get(self.poster_url)
        response_regulations = self.client.get(self.regulations_url)

        # THEN
        self.assertEqual(response_poster.status_code, status.HTTP_200_OK)
        self.assertEqual(response_regulations.status_code, status.HTTP_200_OK)

        self.tearDown()

    def test_get_file_not_authenticated(self):
        # WHEN
        response = self.client.get(self.participant_file_url)

        # THEN
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        self.tearDown()

    def test_delete_file_as_admin(self):
        # GIVEN
        login_data = {'email': 'admin@example.com',
                      'password': 'verylongandsecurepassword'}
        login_response = perform_login(login_data)
        access_token = login_response.data['access']
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {access_token}')

        # WHEN
        response = self.client.delete(self.participant_file_url)

        # THEN
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(
            File.objects.filter(id=self.participant.attachment.id).exists())

        self.tearDown()

    def test_delete_file_as_user_with_permission(self):
        # GIVEN
        login_data = {'email': 'user@example.com',
                      'password': 'verylongandsecurepassword'}
        login_response = perform_login(login_data)
        access_token = login_response.data['access']
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {access_token}')

        # WHEN
        response = self.client.delete(self.participant_file_url)

        # THEN
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

        self.tearDown()

    def test_delete_file_not_authenticated(self):
        # WHEN
        response = self.client.delete(self.participant_file_url)

        # THEN
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

        self.tearDown()
