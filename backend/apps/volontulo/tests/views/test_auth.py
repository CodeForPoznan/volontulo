# -*- coding: utf-8 -*-

"""
.. module:: test_auth
"""

from django.conf import settings
from django.test import Client
from django.test import TestCase

from apps.volontulo.tests import common


class TestLogout(TestCase):
    """Class responsible for testing user logout view."""

    @classmethod
    def setUpTestData(cls):
        """Set up fixtures data for test."""
        # volunteer user
        common.initialize_empty_volunteer()

    def setUp(self):
        """Set up each test."""
        self.client = Client()

    def test__logged_out_anonymous_user(self):
        """Testing logout view for anonymous user"""
        response = self.client.get('/o/logout')
        self.assertRedirects(
            response,
            settings.ANGULAR_ROOT,
            302,
            fetch_redirect_response=False,
        )

    def test__logged_out_authenticated_user(self):
        """Testing logout view for authenticated user."""
        self.client.login(
            username='volunteer1@example.com',
            password='volunteer1',
        )
        response = self.client.get('/o/logout')

        self.assertRedirects(
            response,
            settings.ANGULAR_ROOT,
            302,
            fetch_redirect_response=False,
        )
