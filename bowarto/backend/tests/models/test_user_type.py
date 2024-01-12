from django.test import TestCase
from api.models import UserType


class UserTypeTestCase(TestCase):
    def test_user_type_choices(self):
        # GIVEN
        expected_choices = [('admin', 'Admin'), ('user', 'User')]

        # WHEN
        actual_choices = UserType.choices

        # THEN
        # Assert that the choices method returns the expected list of tuples
        self.assertEqual(actual_choices, expected_choices)

    def test_user_type_from_str_valid_value(self):
        # GIVEN
        valid_str_value = 'Admin'

        # WHEN
        user_type = UserType.from_str(valid_str_value)

        # THEN
        # Assert that the from_str method returns the correct UserTypeEnum
        self.assertEqual(user_type, UserType.ADMIN)

    def test_user_type_from_str_invalid_value(self):
        # GIVEN
        invalid_str_value = 'invalid_type'

        # WHEN
        user_type = UserType.from_str(invalid_str_value)

        # THEN
        # Assert that the from_str method returns None for an invalid value
        self.assertIsNone(user_type)
