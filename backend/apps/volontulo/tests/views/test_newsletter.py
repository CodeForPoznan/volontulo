# -*- coding: utf-8 -*-

"""
.. module:: test_newsletter
"""
from django.test import TestCase


class TestNews(TestCase):
    """Class responsible for testing newsletter specific views."""

    def test__newsletter(self):
        """Test getting newsletter signup page as anonymous."""
        response = self.client.get('/o/newsletter', follow=True)

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'newsletter_signup.html')
