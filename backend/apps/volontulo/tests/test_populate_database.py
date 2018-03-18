"""
.. module:: test_populate_database
"""

from io import StringIO
from unittest import mock

from django.core.files.uploadedfile import SimpleUploadedFile
from django.core.management import call_command
from django.test import TestCase


class PopulateDatabaseTestCase(TestCase):

    """Test for populate_database command."""

    @mock.patch('apps.volontulo.factories.placeimg_com_download')
    def test_command_output(self, placeimg_com_download_mock):
        """Testing if populate_database command get proper output."""
        placeimg_com_download_mock.return_value = lambda: SimpleUploadedFile(
            name='test_image.png',
            content=b'test png content',
        )
        out = StringIO()
        call_command('populate_database', stdout=out)
        self.assertIn('Database successfully populated', out.getvalue())
