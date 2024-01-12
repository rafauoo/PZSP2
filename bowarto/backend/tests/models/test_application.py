from django.test import TestCase
from api.models import Application, Competition, User
from datetime import timedelta
from django.utils import timezone


class ApplicationTestCase(TestCase):
    def setUp(self):
        # Create sample Competition and User for testing
        self.competition = Competition.objects.create(title='Test Competition', start_at=timezone.now(),
                                                      end_at=timezone.now() + timedelta(days=7), )
        self.user = User.objects.create(email='test@example.com', first_name='John', last_name='Doe',
                                        password='password')

    def test_create_application(self):
        # GIVEN
        application_data = {
            'competition': self.competition,
            'user': self.user,
        }

        # WHEN
        application = Application.objects.create(**application_data)

        # THEN
        # Assert that the application is created with the correct data
        self.assertEqual(application.competition, self.competition)
        self.assertEqual(application.user, self.user)

    def test_application_str_method(self):
        # GIVEN
        application = Application.objects.create(competition=self.competition, user=self.user)

        # WHEN
        str_representation = str(application)

        # THEN
        # Assert that the __str__ method returns the expected string representation
        self.assertEqual(str_representation, f"{self.competition.title} - {self.user}")

    def test_create_application_with_null_competition(self):
        # GIVEN
        application_data = {
            'user': self.user,
        }

        # WHEN/THEN: Creating an application without a competition should not raise an exception
        application = Application.objects.create(**application_data)

        # ASSERT
        self.assertIsNone(application.competition)

    def test_create_application_with_null_user(self):
        # GIVEN
        application_data = {
            'competition': self.competition,
        }

        # WHEN/THEN: Creating an application without a user should not raise an exception
        application = Application.objects.create(**application_data)

        # ASSERT
        self.assertIsNone(application.user)
