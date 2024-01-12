from django.test import TestCase
from api.models import Participant, Application, File
from django.core.exceptions import ValidationError


class ParticipantTestCase(TestCase):
    def setUp(self):
        # Create a sample Application and File for testing
        self.application = Application.objects.create()
        self.file = File.objects.create(path='path/to/test.txt')

    def test_create_participant(self):
        # GIVEN
        participant_data = {
            'email': 'test@example.com',
            'application': self.application,
            'first_name': 'John',
            'last_name': 'Doe',
            'attachment': self.file,
        }

        # WHEN
        participant = Participant.objects.create(**participant_data)

        # THEN
        # Assert that the participant is created with the correct data
        self.assertEqual(participant.email, 'test@example.com')
        self.assertEqual(participant.application, self.application)
        self.assertEqual(participant.first_name, 'John')
        self.assertEqual(participant.last_name, 'Doe')
        self.assertEqual(participant.attachment, self.file)

    def test_create_participant_without_email(self):
        # GIVEN
        participant_data = {
            'application': self.application,
            'first_name': 'John',
            'last_name': 'Doe',
        }

        # WHEN/THEN: Creating a participant without email should not raise an exception
        participant = Participant.objects.create(**participant_data)

        # ASSERT
        self.assertIsNone(participant.email)

    def test_create_participant_without_attachment(self):
        # GIVEN
        participant_data = {
            'email': 'test@example.com',
            'application': self.application,
            'first_name': 'John',
            'last_name': 'Doe',
        }

        # WHEN/THEN: Creating a participant without attachment should not raise an exception
        participant = Participant.objects.create(**participant_data)

        # ASSERT
        self.assertIsNone(participant.attachment)

    def test_create_participant_with_invalid_email(self):
        # GIVEN
        participant_data = {
            'email': 'invalid-email',  # Invalid email format
            'application': self.application,
            'first_name': 'John',
            'last_name': 'Doe',
        }

        # WHEN/THEN: Creating a participant with an invalid email should raise a ValidationError
        with self.assertRaises(ValidationError):
            Participant.objects.create(**participant_data)

    def test_participant_str_method(self):
        # GIVEN
        participant = Participant.objects.create(
            email='test@example.com',
            application=self.application,
            first_name='John',
            last_name='Doe',
            attachment=self.file,
        )

        # WHEN
        str_representation = str(participant)

        # THEN
        # Assert that the __str__ method returns the expected string representation
        self.assertEqual(str_representation, 'John Doe')
