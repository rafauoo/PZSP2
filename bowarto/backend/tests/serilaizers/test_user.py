from django.test import TestCase
from django.core.exceptions import ValidationError
from api.models import User, UserType
from api.serializers.user import UserSerializer, UserRegistrationSerializer


class UserRegistrationSerializerTest(TestCase):
    def test_create_user_registration(self):
        data = {
            'email': 'test@example.com',
            'password': 'TestPassword123',
            'first_name': 'John',
            'last_name': 'Doe',
        }

        serializer = UserRegistrationSerializer(data=data)
        self.assertTrue(serializer.is_valid())
        user = serializer.save()

        self.assertEqual(user.email, 'test@example.com')
        self.assertEqual(user.first_name, 'John')
        self.assertEqual(user.last_name, 'Doe')
        self.assertTrue(user.check_password('TestPassword123'))
        self.assertEqual(user.user_type, UserType.USER.value)

    def test_create_user_with_weak_password(self):
        data = {
            'email': 'test_user@example.com',
            'password': '123',
            'first_name': 'John',
            'last_name': 'Doe',
        }

        serializer = UserRegistrationSerializer(data=data)
        self.assertFalse(serializer.is_valid())
