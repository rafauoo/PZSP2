from django.test import TestCase
from api.models import School, PendingApproval, User
from api.serializers.pending_approval import PendingApprovalSerializer
from rest_framework import serializers


class PendingApprovalSerializerTest(TestCase):
    def setUp(self):
        # Utwórz przykładowego użytkownika Django
        self.user = User.objects.create(email='test@example.com', first_name='John', last_name='Doe',
                                        password='password')
        # Utwórz przykładową szkołę
        self.school = School.objects.create(
            name='Test School',
            phone_number='123-456-789',
            email='school@example.com',
            city='Test City',
            street='Test Street',
            building_number='123',
            postcode='00-000'
        )

    def test_pending_approval_serializer_valid_data(self):
        # Sprawdź, czy serializer poprawnie obsługuje poprawne dane
        data = {'user': self.user.id, 'school': self.school.id}
        serializer = PendingApprovalSerializer(data=data)
        self.assertTrue(serializer.is_valid())

    def test_pending_approval_serializer_missing_user(self):
        # Sprawdź, czy serializer zgłasza błąd, gdy brakuje użytkownika
        data = {'school': self.school.id}
        serializer = PendingApprovalSerializer(data=data)
        self.assertFalse(serializer.is_valid())
        self.assertIn('user', serializer.errors)
        self.assertEqual(serializer.errors['user'][0], "This field is required.")

        with self.assertRaises(serializers.ValidationError):
            serializer.validate(data=data)

    def test_pending_approval_serializer_missing_school(self):
        # Sprawdź, czy serializer zgłasza błąd, gdy brakuje szkoły
        data = {'user': self.user.id}
        serializer = PendingApprovalSerializer(data=data)
        self.assertFalse(serializer.is_valid())
        self.assertIn('school', serializer.errors)
        self.assertEqual(serializer.errors['school'][0], "This field is required.")

        with self.assertRaises(serializers.ValidationError):
            serializer.validate(data=data)
