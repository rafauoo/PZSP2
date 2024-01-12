from django.test import TestCase
from api.models import User, School, PendingApproval


class PendingApprovalTest(TestCase):
    def setUp(self):
        # Tworzenie przykładowego użytkownika
        self.user = User.objects.create(email='test@example.com', first_name='John', last_name='Doe',
                                        password='password')

        # Tworzenie przykładowej szkoły
        self.school = School.objects.create(
            name='Test School',
            phone_number='123-456-789',
            email='school@example.com',
            city='Test City',
            street='Test Street',
            building_number='123',
            postcode='00-000'
        )

    def test_pending_approval_creation(self):
        # Sprawdzenie, czy obiekt PendingApproval został poprawnie utworzony
        pending_approval = PendingApproval.objects.create(user=self.user, school=self.school)
        self.assertEqual(str(pending_approval), f"Pending Approval: user: {self.user}, school: {self.school}")

    def test_pending_approval_str_method(self):
        # Sprawdzenie, czy metoda __str__ zwraca oczekiwany rezultat
        pending_approval = PendingApproval.objects.create(user=self.user, school=self.school)
        expected_str = f"Pending Approval: user: {self.user}, school: {self.school}"
        self.assertEqual(str(pending_approval), expected_str)

    def test_pending_approval_deletion(self):
        # Sprawdzenie, czy obiekt PendingApproval zostaje poprawnie usunięty
        pending_approval = PendingApproval.objects.create(user=self.user, school=self.school)
        pending_approval_id = pending_approval.id
        pending_approval.delete()

        # Sprawdzenie, czy obiekt nie istnieje po usunięciu
        with self.assertRaises(PendingApproval.DoesNotExist):
            PendingApproval.objects.get(id=pending_approval_id)
