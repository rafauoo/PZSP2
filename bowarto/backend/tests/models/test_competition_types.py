from django.test import TestCase
from api.models import CompetitionType


class CompetitionTypeTestCase(TestCase):
    def test_competition_type_choices(self):
        # GIVEN
        expected_choices = [
            ('artystyczny', 'Artystyczny'),
            ('fotograficzny', 'Fotograficzny'),
            ('literacki', 'Literacki'),
            ('inny', 'Inny')
        ]

        # WHEN
        actual_choices = CompetitionType.choices

        # THEN
        # Assert that the choices method returns the expected list of tuples
        self.assertEqual(actual_choices, expected_choices)

    def test_competition_type_from_str_valid_value(self):
        # GIVEN
        valid_str_value = 'artystyczny'

        # WHEN
        competition_type = CompetitionType.from_str(valid_str_value)

        # THEN
        # Assert that the from_str method returns the correct CompetitionTypeEnum
        self.assertEqual(competition_type, CompetitionType.ARTISTIC)

    def test_competition_type_from_str_invalid_value(self):
        # GIVEN
        invalid_str_value = 'invalid_type'

        # WHEN
        competition_type = CompetitionType.from_str(invalid_str_value)

        # THEN
        # Assert that the from_str method returns None for an invalid value
        self.assertIsNone(competition_type)
