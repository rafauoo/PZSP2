from django.test import TestCase
from api.models import CompetitionType
from api.serializers.competition_type import CompetitionTypeSerializer
from rest_framework.exceptions import ValidationError


class CompetitionTypeSerializerTest(TestCase):

    def test_serialize_competition_type(self):
        competition_type = CompetitionType.ARTISTIC
        serializer = CompetitionTypeSerializer(competition_type)
        data = serializer.data

        self.assertIn('name', data)
        self.assertEqual(data['name'], 'artystyczny')

    def test_invalid_input(self):
        invalid_input = {'name': 'Invalid Name'}
        serializer = CompetitionTypeSerializer(data=invalid_input)

        with self.assertRaises(ValidationError):
            serializer.is_valid(raise_exception=True)

    def test_read_only_field(self):
        competition_type = CompetitionType.PHOTOGRAPHIC
        serializer = CompetitionTypeSerializer()

        with self.assertRaises(ValidationError):
            setattr(serializer, 'initial_data', {'name': competition_type.value})
            serializer.is_valid(raise_exception=True)
