from django.test import TestCase
from api.models import School


class SchoolModelTest(TestCase):
    def setUp(self):
        # GIVEN
        self.school_data = {
            'name': 'Test School',
            'phone_number': '123-456-7890',
            'email': 'test@example.com',
            'city': 'Test City',
            'street': 'Test Street',
            'building_number': '123',
            'postcode': '12345'
        }

    def test_create_school(self):
        # GIVEN
        # WHEN
        school = School.objects.create(**self.school_data)
        # THEN
        self.assertEqual(school.name, 'Test School')
        self.assertEqual(school.phone_number, '123-456-7890')
        self.assertEqual(school.email, 'test@example.com')
        self.assertEqual(school.city, 'Test City')
        self.assertEqual(school.street, 'Test Street')
        self.assertEqual(school.building_number, '123')
        self.assertEqual(school.postcode, '12345')

    def test_unique_email(self):
        # GIVEN
        School.objects.create(**self.school_data)
        # WHEN
        with self.assertRaises(Exception):
            School.objects.create(**self.school_data)
        # THEN

    def test_optional_fields(self):
        # GIVEN
        school_data_optional = {
            'name': 'Test School 2',
            'phone_number': '987-654-3210',
            'email': 'test2@example.com',
            'city': 'Test City 2',
            'street': 'Test Street 2',
            'building_number': '456',
            'postcode': '54321',
        }
        # WHEN
        school = School.objects.create(**school_data_optional)
        # THEN
        self.assertIsNone(school.fax_number)
        self.assertIsNone(school.website)
        self.assertIsNone(school.apartment_number)

    def test_str_method(self):
        # GIVEN
        school = School.objects.create(**self.school_data)
        # WHEN
        result = str(school)
        # THEN
        self.assertEqual(result, 'Test School')

    def test_create_school_without_optional_fields(self):
        # GIVEN
        school_data_without_optional = {
            'name': 'Test School 3',
            'phone_number': '111-222-3333',
            'email': 'test3@example.com',
            'city': 'Test City 3',
            'street': 'Test Street 3',
            'building_number': '789',
            'postcode': '98765',
        }
        # WHEN
        school = School.objects.create(**school_data_without_optional)
        # THEN
        self.assertIsNone(school.fax_number)
        self.assertIsNone(school.website)
        self.assertIsNone(school.apartment_number)

    def test_create_school_with_all_fields(self):
        # GIVEN
        school_data_all_fields = {
            'name': 'Test School 4',
            'phone_number': '444-555-6666',
            'fax_number': '444-555-7777',
            'email': 'test4@example.com',
            'website': 'http://www.test4.com',
            'city': 'Test City 4',
            'street': 'Test Street 4',
            'building_number': '987',
            'apartment_number': '456',
            'postcode': '56789',
        }
        # WHEN
        school = School.objects.create(**school_data_all_fields)
        # THEN
        self.assertEqual(school.fax_number, '444-555-7777')
        self.assertEqual(school.website, 'http://www.test4.com')
        self.assertEqual(school.apartment_number, '456')
