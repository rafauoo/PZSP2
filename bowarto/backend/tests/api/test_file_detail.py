from django.test import TestCase
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient
from unittest.mock import patch
from django.core.files.uploadedfile import SimpleUploadedFile
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
