from datetime import datetime, timedelta
from django.test import TestCase
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient
from api.models import User, School, Competition, Application, Participant, \
    PendingApproval, UserType

from tests.utils import perform_login

from tests.setup import create_admin


class StatsViewTest(TestCase):
    def setUp(self):
        self.client = APIClient()

        # Create a user
        self.user = create_admin(
            email='admin@example.com',
            password='securepassword'
        )

        # Create a school
        self.school = School.objects.create(
            name='Example School',
            phone_number='123-456-7890',
            email='school@example.com',
            city='Cityville',
            street='Main Street',
            building_number='123',
            postcode='ABCDE'
        )

        # Create a competition
        self.competition = Competition.objects.create(
            title='Test Competition',
            description='This is a test competition',
            type='artystyczny',
            start_at=datetime.now() - timedelta(days=2),
            end_at=datetime.now() + timedelta(days=2),
        )

        # Create an application
        self.application = Application.objects.create(
            competition=self.competition,
            user=self.user
        )

        # Create a participant
        self.participant = Participant.objects.create(
            email='participant@example.com',
            application=self.application,
            first_name='Participant',
            last_name='Example'
        )

        # Create a pending approval
        self.pending_approval = PendingApproval.objects.create(
            user=self.user,
            school=self.school
        )

    def test_stats_view_authenticated_user(self):
        # Log in the user
        login_data = {'email': 'admin@example.com',
                      'password': 'securepassword'}
        login_response = perform_login(login_data)
        access_token = login_response.data['access']
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {access_token}')

        # Make a GET request to the StatsView
        url = reverse('stats')
        response = self.client.get(url)

        # Check that the response status code is 200 OK
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        # Check the expected number of ongoing competitions
        self.assertEqual(response.data['ongoing_competitions_count'], 1)

        # Check the expected number of upcoming competitions
        self.assertEqual(response.data['upcoming_competitions_count'], 0)

        # Check the expected number of finished competitions
        self.assertEqual(response.data['finished_competitions_count'], 0)

    def test_stats_view_unauthenticated_user(self):
        # Make a GET request to the StatsView without authenticating the user
        url = reverse('stats')
        response = self.client.get(url)

        # Check that the response status code is 401 Unauthorized
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
