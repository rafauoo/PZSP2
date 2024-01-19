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

    def test_save_method(self):
        # GIVEN
        competition_data = {
            'title': 'Test Competition',
            'start_at': timezone.now(),
            'end_at': timezone.now() + timedelta(days=7),
        }

        # WHEN
        competition = Competition(**competition_data)
        competition.save()

        # ASSERT
        self.assertEqual(Competition.objects.count(), 1)

    def test_clean_method_invalid_dates(self):
        # GIVEN
        competition_data = {
            'title': 'Test Competition',
            'start_at': timezone.now(),
            'end_at': timezone.now() - timedelta(days=7),  # Invalid end date
        }

        # WHEN/THEN: Creating a competition with invalid dates should raise a ValidationError
        with self.assertRaises(ValidationError) as context:
            competition = Competition(**competition_data)
            competition.clean()

        # ASSERT
        self.assertIn("End date must be greater than the start date.",
                      str(context.exception))

    def test_clean_method_invalid_competition_type(self):
        # GIVEN
        competition_data = {
            'title': 'Test Competition',
            'start_at': timezone.now(),
            'end_at': timezone.now() + timedelta(days=7),
            'type': 'InvalidType',  # Invalid competition type
        }

        # WHEN/THEN: Creating a competition with an invalid competition type should raise a ValidationError
        with self.assertRaises(ValidationError) as context:
            competition = Competition(**competition_data)
            competition.clean()

        # ASSERT
        self.assertIn("Invalid competition type.", str(context.exception))

    def test_delete_method(self):
        # GIVEN
        file1 = File.objects.create(path='path/to/poster.png')
        file2 = File.objects.create(path='path/to/regulation.pdf')

        competition_data = {
            'title': 'Test Competition',
            'start_at': timezone.now(),
            'end_at': timezone.now(),
            'poster': file1,
            'regulation': file2,
        }

        # WHEN
        competition = Competition.objects.create(**competition_data)
        competition_id = competition.id

        # Ensure that the files are associated with the competition
        self.assertIsNotNone(competition.poster)
        self.assertIsNotNone(competition.regulation)

        # THEN
        # Deleting the competition should also delete associated files
        competition.delete()

        # ASSERT
        # Ensure that the competition and associated files are deleted from the database
        self.assertEqual(Competition.objects.filter(id=competition_id).count(),
                         0)
        self.assertEqual(File.objects.filter(id=file1.id).count(), 0)
        self.assertEqual(File.objects.filter(id=file2.id).count(), 0)
