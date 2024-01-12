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

        self.admin = create_admin('admin@example.com', '123')
        self.user = create_user('user@example.com', '123')

        self.school = School.objects.create(
            name='School',
            phone_number='123456789',
            email='school1@example.com',
            city='City 1',
            street='Street 1',
            building_number='1',
            postcode='12345'
        )

        # Utwórz zgłoszenie
        self.pending_approval = PendingApproval.objects.create(
            user=self.user,
            school=self.school)

        self.url = reverse('approval-detail', kwargs={'id': self.pending_approval.id})

    def test_get_pending_approval_as_admin(self):
        # GIVEN
        login_data = {'email': 'admin@example.com', 'password': '123'}
        login_response = perform_login(login_data)
        self.access_token = login_response.data['access']
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {self.access_token}')

        # WHEN
        response = self.client.get(self.url)

        # THEN
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_delete_pending_approval_as_admin(self):
        # GIVEN
        login_data = {'email': 'admin@example.com', 'password': '123'}
        login_response = perform_login(login_data)
        self.access_token = login_response.data['access']
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {self.access_token}')

        # WHEN
        response = self.client.delete(self.url)

        # THEN
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertIsNone(PendingApproval.objects.filter(id=self.pending_approval.id).first())

        self.user.refresh_from_db()
        self.assertEqual(self.user.school, self.pending_approval.school)

    def test_get_pending_approval_as_user(self):
        # GIVEN
        login_data = {'email': 'user@example.com', 'password': '123'}
        login_response = perform_login(login_data)
        self.access_token = login_response.data['access']
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {self.access_token}')

        # WHEN
        response = self.client.get(self.url)

        # THEN
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_delete_pending_approval_as_user(self):
        # GIVEN
        login_data = {'email': 'user@example.com', 'password': '123'}
        login_response = perform_login(login_data)
        self.access_token = login_response.data['access']
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {self.access_token}')

        # WHEN
        response = self.client.delete(self.url)

        # THEN
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertIsNotNone(PendingApproval.objects.filter(id=self.pending_approval.id).first())

        self.user.refresh_from_db()
        self.assertIsNone(self.user.school)
