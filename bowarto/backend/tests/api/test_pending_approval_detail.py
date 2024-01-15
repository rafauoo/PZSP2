from django.test import TestCase
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient

from api.models import PendingApproval, School
from api.serializers.pending_approval import PendingApprovalSerializer
from tests.setup import create_admin, create_user
from tests.utils import perform_login


class TestPendingApprovalDetail(TestCase):
    def setUp(self):
        self.client = APIClient()

        self.admin = create_admin('admin@example.com',
                                  'verylongandsecurepassword')
        self.user = create_user('user@example.com', 'verylongandsecurepassword')

        self.school = School.objects.create(
            name='School',
            phone_number='verylongandsecurepassword456789',
            email='school1@example.com',
            city='City 1',
            street='Street 1',
            building_number='1',
            postcode='verylongandsecurepassword45'
        )

        # Utwórz zgłoszenie
        self.pending_approval = PendingApproval.objects.create(
            user=self.user,
            school=self.school)

        self.url = reverse('approval-detail',
                           kwargs={'id': self.pending_approval.id})

    def test_get_pending_approval_as_admin(self):
        # GIVEN
        login_data = {'email': 'admin@example.com',
                      'password': 'verylongandsecurepassword'}
        login_response = perform_login(login_data)
        self.access_token = login_response.data['access']
        self.client.credentials(
            HTTP_AUTHORIZATION=f'Bearer {self.access_token}')

        # WHEN
        response = self.client.get(self.url)

        # THEN
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_get_pending_approval_as_user(self):
        # GIVEN
        login_data = {'email': 'user@example.com',
                      'password': 'verylongandsecurepassword'}
        login_response = perform_login(login_data)
        self.access_token = login_response.data['access']
        self.client.credentials(
            HTTP_AUTHORIZATION=f'Bearer {self.access_token}')

        # WHEN
        response = self.client.get(self.url)

        # THEN
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
