from django.test import TestCase
from django.contrib.auth import get_user_model
from api.models import UserType


class CustomUserManagerTests(TestCase):
    def test_create_user(self):
        User = get_user_model()
        email = "test@example.com"
        password = "testpassword"
        user = User.objects.create_user(email=email, password=password, first_name="John", last_name="Doe")

        self.assertEqual(user.email, email)
        self.assertTrue(user.check_password(password))
        self.assertEqual(user.user_type, UserType.USER.value)
        self.assertEqual(user.first_name, "John")
        self.assertEqual(user.last_name, "Doe")

    def test_create_superuser(self):
        User = get_user_model()
        email = "admin@example.com"
        password = "adminpassword"
        superuser = User.objects.create_superuser(email=email, password=password, first_name="Admin", last_name="User")

        self.assertEqual(superuser.email, email)
        self.assertTrue(superuser.check_password(password))
        self.assertEqual(superuser.user_type, UserType.ADMIN.value)
        self.assertTrue(superuser.is_admin)
        self.assertEqual(superuser.first_name, "Admin")
        self.assertEqual(superuser.last_name, "User")

    def test_create_user_with_custom_fields(self):
        User = get_user_model()
        email = "test@example.com"
        password = "testpassword"
        user_type = UserType.USER.value
        first_name = "John"
        last_name = "Doe"
        user = User.objects.create_user(email=email, password=password, user_type=user_type, first_name=first_name,
                                        last_name=last_name)

        self.assertEqual(user.email, email)
        self.assertTrue(user.check_password(password))
        self.assertEqual(user.user_type, user_type)
        self.assertEqual(user.first_name, first_name)
        self.assertEqual(user.last_name, last_name)

    def test_create_user_with_missing_email(self):
        User = get_user_model()
        password = "testpassword"

        with self.assertRaises(ValueError) as context:
            User.objects.create_user(email="", password=password, first_name="John", last_name="Doe")

        self.assertEqual(str(context.exception), "The Email field must be set")

    def test_create_superuser_with_missing_email(self):
        User = get_user_model()
        password = "adminpassword"

        with self.assertRaises(ValueError) as context:
            User.objects.create_superuser(email="", password=password, first_name="Admin", last_name="User")

        self.assertEqual(str(context.exception), "The Email field must be set")
