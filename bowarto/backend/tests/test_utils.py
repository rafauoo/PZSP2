import unittest
from unittest.mock import MagicMock
from api.utils import is_allowed_file_type


class TestIsAllowedFileType(unittest.TestCase):

    def test_pdf_file(self):
        # GIVEN
        pdf_content = b'%PDF-1.4 ...'  # Sample PDF file content

        # WHEN
        result = is_allowed_file_type(pdf_content)

        # THEN
        self.assertTrue(result)

    def test_jpeg_image_file(self):
        # GIVEN
        jpeg_content = b'\xff\xd8\xff\xe0\x00\x10JFIF\x00\x01\x01...'  # Sample JPEG image content

        # WHEN
        result = is_allowed_file_type(jpeg_content)

        # THEN
        self.assertTrue(result)

    def test_png_image_file(self):
        # GIVEN
        png_content = b'\x89PNG\r\n\x1a\n\x00\x00\x00\rIHDR\x00\x00...'  # Sample PNG image content

        # WHEN
        result = is_allowed_file_type(png_content)

        # THEN
        self.assertTrue(result)

    def test_invalid_file(self):
        # GIVEN
        invalid_content = b'Invalid file content'

        # WHEN
        result = is_allowed_file_type(invalid_content)

        # THEN
        self.assertFalse(result)

    def test_empty_file(self):
        # GIVEN
        empty_content = b''

        # WHEN
        result = is_allowed_file_type(empty_content)

        # THEN
        self.assertFalse(result)

    def test_mocked_magic_library(self):
        # GIVEN
        mocked_magic = MagicMock()
        mocked_magic.return_value.from_buffer.return_value = 'application/pdf'
        with unittest.mock.patch('magic.Magic', mocked_magic):
            # WHEN
            result = is_allowed_file_type(b'Sample content')

        # THEN
        self.assertTrue(result)
