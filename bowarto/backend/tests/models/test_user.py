from django.test import TestCase
from django.core.exceptions import ValidationError
from api.models import User, UserType, School


class UserTestCase(TestCase):
    def test_create_user_default(self):
        # GIVEN
        user_data = {
            'email': 'test@example.com',
            'first_name': 'John',
            'last_name': 'Doe',
            'password': 'testpassword123',
        }

        # WHEN
        user = User.objects.create(**user_data)

        # THEN
        self.assertEqual(user.email, 'test@example.com')
        self.assertEqual(user.first_name, 'John')
        self.assertEqual(user.last_name, 'Doe')
        self.assertEqual(user.password, 'testpassword123')
        self.assertEqual(user.user_type, UserType.USER.value)
        self.assertTrue(user.is_user)

    def test_create_observer(self):
        # GIVEN
        user_data = {
            'email': 'test@example.com',
            'first_name': 'John',
            'last_name': 'Doe',
            'password': 'testpassword123',
            'user_type': UserType.OBSERVER.value
        }

        # WHEN
        user = User.objects.create(**user_data)

        # THEN
        self.assertEqual(user.email, 'test@example.com')
        self.assertEqual(user.first_name, 'John')
        self.assertEqual(user.last_name, 'Doe')
        self.assertEqual(user.password, 'testpassword123')
        self.assertEqual(user.user_type, UserType.OBSERVER.value)
        self.assertTrue(user.is_observer)

    def test_create_admin_with_school(self):
        # GIVEN
        user_data = {
            'email': 'test@example.com',
            'first_name': 'John',
            'last_name': 'Doe',
            'user_type': UserType.ADMIN.value,
            'password': 'testpassword123',
            'school': {
                'name': 'Example School',
                'phone_number': '123456789',
                'email': 'school@example.com',
                'city': 'City',
                'street': 'Street',
                'building_number': '123',
                'postcode': '12345',
            }
        }

        # WHEN
        with self.assertRaises(ValidationError):
            User.objects.create(
                email=user_data['email'],
                first_name=user_data['first_name'],
                last_name=user_data['last_name'],
                user_type=user_data['user_type'],
                password=user_data['password'],
                school=School.objects.create(**user_data['school']),
            )

        # THEN
        # Assert that ValidationError is raised when creating a admin with a school

    def test_create_user_with_school(self):
        # GIVEN
        user_data = {
            'email': 'test@example.com',
            'first_name': 'John',
            'last_name': 'Doe',
            'user_type': UserType.USER.value,
            'password': 'testpassword123',
            'school': {
                'name': 'Example School',
                'phone_number': '123456789',
                'email': 'school@example.com',
                'city': 'City',
                'street': 'Street',
                'building_number': '123',
                'postcode': '12345',
            }
        }

        # WHEN
        user = User.objects.create(
            email=user_data['email'],
            first_name=user_data['first_name'],
            last_name=user_data['last_name'],
            user_type=user_data['user_type'],
            password=user_data['password'],
            school=School.objects.create(**user_data['school']),
        )

        # THEN
        self.assertEqual(user.school.name, user_data['school']['name'])

    def test_create_user_with_invalid_type(self):
        # GIVEN
        user_data = {
            'email': 'test@example.com',
            'first_name': 'John',
            'last_name': 'Doe',
            'password': 'testpassword123',
            'user_type': UserType.USER.value + 'sus'
        }
        # WHEN
        with self.assertRaises(ValidationError):
            User.objects.create(**user_data)

        # THEN

    def test_save_user(self):
        # GIVEN
        user_data = {
            'email': 'test@example.com',
            'first_name': 'John',
            'last_name': 'Doe',
            'password': 'testpassword123',
            'user_type': UserType.USER.value
        }

        # WHEN
        user = User.objects.create(**user_data)
        user.save()

        # THEN
        # Assert that saving a user with valid data does not raise any exceptions

    def test_update_user_type(self):
        # GIVEN
        user_data = {
            'email': 'test@example.com',
            'first_name': 'John',
            'last_name': 'Doe',
            'user_type': UserType.USER.value,
            'password': 'password123'
        }
        user = User.objects.create(**user_data)

        # WHEN
        user.user_type = UserType.OBSERVER.value

        # THEN
        with self.assertRaises(ValidationError):
            user.save()

    def test_save_user_with_invalid_type(self):
        # GIVEN
        user_data = {
            'email': 'test@example.com',
            'first_name': 'John',
            'last_name': 'Doe',
            'password': 'testpassword123',
            'user_type': UserType.USER.value + 'sus'
        }

        # WHEN
        with self.assertRaises(ValidationError):
            User.objects.create(**user_data)
