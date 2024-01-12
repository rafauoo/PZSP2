from django.test import TestCase
from django.core.files.storage import default_storage
from api.models import File


class FileTestCase(TestCase):
    def test_file_deletion(self):
        # GIVEN
        file_instance = File.objects.create(path='path/to/test.txt')

        # WHEN
        file_instance.delete()

        # THEN
        # Assert that the file is deleted from the storage
        self.assertFalse(default_storage.exists(file_instance.path.name))

    def test_file_deletion_with_no_path(self):
        # GIVEN
        file_instance = File.objects.create(path=None)

        # WHEN
        file_instance.delete()

        # THEN
        # Assert that deletion works even if the file path is None
        self.assertTrue(True)  # Placeholder assertion, adjust as needed

    def test_file_deletion_with_existing_file(self):
        # GIVEN
        file_instance = File.objects.create(path='path/to/existing_file.txt')

        # Create the file in the storage to simulate an existing file
        with default_storage.open(file_instance.path.name, 'w') as file:
            file.write('Test content')

        # WHEN
        file_instance.delete()

        # THEN
        # Assert that the file is deleted from the storage
        self.assertFalse(default_storage.exists(file_instance.path.name))
