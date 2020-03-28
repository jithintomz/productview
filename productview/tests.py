from django.test import TestCase

from productview.models import Upload


class ModelTestCase(TestCase):
    def test_upload(self):
        upload = Upload(file_name="Test File")
        self.assertEqual(upload.file_name, "Test File")
