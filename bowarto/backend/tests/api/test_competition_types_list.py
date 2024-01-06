from django.test import TestCase
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient
from api.models import CompetitionType
from api.serializers.competition_type import CompetitionTypeSerializer
from api.views.competition_type import CompetitionTypeList
from tests.setup import create_admin, create_user
from tests.utils import perform_login


class CompetitionTypeListTests(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.url = reverse('competition_type-list')

        # Utwórz kilka przykładowych typów konkursów do testowania
        self.competition_type1 = CompetitionType.objects.create(name='Artystyczny')
        self.competition_type2 = CompetitionType.objects.create(name='Fotograficzny')

    def test_list_competition_types(self):
        # WHEN
        response = self.client.get(self.url)

        # THEN
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        serializer = CompetitionTypeSerializer(CompetitionType.objects.all(), many=True)
        self.assertEqual(response.data, serializer.data)
