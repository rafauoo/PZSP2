from django.test import TestCase
from django.core.exceptions import ValidationError
from api.models import Competition, CompetitionType, File
from datetime import timedelta
from django.utils import timezone


class CompetitionTestCase(TestCase):
    def test_valid_competition(self):
        # GIVEN
        competition_data = {
            'title': 'Test Competition',
            'description': 'Description of the competition',
            'type': CompetitionType.ARTISTIC,
            'start_at': timezone.now(),
            'end_at': timezone.now() + timedelta(days=7),
        }

        # WHEN/THEN: Creating a competition with valid data should not raise an exception
        competition = Competition.objects.create(**competition_data)

        # ASSERT
        self.assertEqual(Competition.objects.count(), 1)
        title = competition.__str__()
        self.assertEqual(title, 'Test Competition')

    def test_invalid_end_date(self):
        # GIVEN
        competition_data = {
            'title': 'Test Competition',
            'start_at': timezone.now(),
            'end_at': timezone.now() - timedelta(days=7),  # End date is before start date
        }

        # WHEN/THEN: Creating a competition with an invalid end date should raise a ValidationError
        with self.assertRaises(ValidationError):
            Competition.objects.create(**competition_data)

    def test_invalid_competition_type(self):
        # GIVEN
        competition_data = {
            'title': 'Test Competition',
            'type': 'invalid_type',  # Invalid competition type
            'start_at': timezone.now(),
            'end_at': timezone.now() + timedelta(days=7),
        }

        # WHEN/THEN: Creating a competition with an invalid competition type should raise a ValidationError
        with self.assertRaises(ValidationError):
            Competition.objects.create(**competition_data)

    def test_valid_file_association(self):
        # GIVEN
        file = File.objects.create(path='path/to/test.png')
        competition_data = {
            'title': 'Test Competition',
            'start_at': timezone.now(),
            'end_at': timezone.now() + timedelta(days=7),
            'poster': file,
            'regulation': file,
        }

        # WHEN/THEN: Creating a competition with valid file associations should not raise an exception
        competition = Competition.objects.create(**competition_data)

        # ASSERT
        self.assertEqual(Competition.objects.count(), 1)
