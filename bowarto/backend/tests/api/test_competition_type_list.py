from django.test import TestCase
from django.urls import reverse
from rest_framework.test import APIClient
from rest_framework import status

from api.models import CompetitionType


class CompetitionTypeListTest(TestCase):

    def setUp(self):
        self.client = APIClient()
        self.url = reverse('competition-type-list')

        # Dodaj przykładowe rodzaje konkursów
        self.artistic_type = CompetitionType.ARTISTIC
        self.photographic_type = CompetitionType.PHOTOGRAPHIC

    def test_list_competition_types(self):
        # WHEN
        response = self.client.get(self.url)

        # THEN
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 4)  # Zakładając, że masz 4 rodzaje konkursów

    def test_unauthenticated_request(self):
        # WHEN
        response = self.client.get(self.url)

        # THEN
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), len(CompetitionType))
