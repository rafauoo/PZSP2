from django.test import TestCase
from django.urls import reverse
from rest_framework.test import APIClient
from rest_framework import status

from api.models import PendingApproval, School
from api.serializers.pending_approval import PendingApprovalSerializer
from tests.setup import create_admin, create_user
from tests.utils import perform_login


class TestPendingApprovalList(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.url = reverse('approval-list')

        self.admin = create_admin('admin@example.com', 'verylongandsecurepassword')
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

    def test_list_pending_approvals_as_admin(self):
        # GIVEN
        login_data = {'email': 'admin@example.com', 'password': 'verylongandsecurepassword'}
        login_response = perform_login(login_data)
        access_token = login_response.data['access']
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {access_token}')

        # WHEN
        response = self.client.get(self.url)

        # THEN
        approvals = PendingApproval.objects.all()
        serializer = PendingApprovalSerializer(approvals, many=True)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, serializer.data)

    def test_list_pending_approvals_as_user(self):
        # GIVEN
        login_data = {'email': 'user@example.com', 'password': 'verylongandsecurepassword'}
        login_response = perform_login(login_data)
        access_token = login_response.data['access']
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {access_token}')

        # WHEN
        response = self.client.get(self.url)

        # THEN
        approvals = PendingApproval.objects.all()

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_list_pending_approvals_not_authenticated(self):
        # GIVEN

        # WHEN
        response = self.client.get(self.url)

        # THEN
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_create_pending_approval_as_admin(self):
        # GIVEN
        login_data = {'email': 'admin@example.com', 'password': 'verylongandsecurepassword'}
        login_response = perform_login(login_data)
        access_token = login_response.data['access']
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {access_token}')

        # WHEN
        data = {'school': self.school.id}
        response = self.client.post(self.url, data)

        # THEN
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_create_pending_approval_as_user(self):
        # GIVEN
        login_data = {'email': 'user@example.com', 'password': 'verylongandsecurepassword'}
        login_response = perform_login(login_data)
        access_token = login_response.data['access']
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {access_token}')

        # WHEN
        data = {'school': self.school.id}
        response = self.client.post(self.url, data)

        # THEN
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_create_pending_approval_not_authenticated(self):
        # GIVEN

        # WHEN
        data = {'school': self.school.id}
        response = self.client.post(self.url, data)

        # THEN
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_create_pending_approval_no_school(self):
        # GIVEN
        login_data = {'email': 'user@example.com', 'password': 'verylongandsecurepassword'}
        login_response = perform_login(login_data)
        access_token = login_response.data['access']
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {access_token}')

        # WHEN
        data = {}
        response = self.client.post(self.url, data)

        # THEN
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
