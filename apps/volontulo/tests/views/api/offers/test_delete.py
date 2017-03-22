# -*- coding: utf-8 -*-

"""
.. module:: test_delete
"""

from rest_framework import status
from rest_framework.test import APITestCase

from apps.volontulo.tests.views.offers.commons import TestOffersCommons


class TestAdminUserOffersDeleteAPIView(TestOffersCommons, APITestCase):

    """Tests for REST API's delete offer view for admin user."""

    def setUp(self):
        """Set up each test."""
        super(TestAdminUserOffersDeleteAPIView, self).setUp()
        self.client.login(username='admin@example.com', password='123admin')

    def test_offer_delete_status(self):
        """Test offer's delete status for admin user.

        API for now is read-only.
        """
        response = self.client.delete('/api/offers/1/')

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)


class TestOrganizationUserOffersDeleteAPIView(TestOffersCommons, APITestCase):

    """Tests for REST API's delete offer view for user with organization."""

    def setUp(self):
        """Set up each test."""
        super(TestOrganizationUserOffersDeleteAPIView, self).setUp()
        self.client.login(
            username='cls.organization@example.com',
            password='123org'
        )

    def test_offer_delete_status(self):
        """Test offer's delete status for user with organization.

        API for now is read-only.
        """
        response = self.client.delete('/api/offers/1/')

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)


class TestRegularUserOffersDeleteAPIView(TestOffersCommons, APITestCase):

    """Tests for REST API's delete offer view for regular user."""

    def setUp(self):
        """Set up each test."""
        super(TestRegularUserOffersDeleteAPIView, self).setUp()
        self.client.login(
            username='volunteer@example.com',
            password='123volunteer'
        )

    def test_offer_delete_status(self):
        """Test offer's delete status for regular user.

        API for now is read-only.
        """
        response = self.client.delete('/api/offers/1/')

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)


class TestAnonymousUserOffersDeleteAPIView(TestOffersCommons, APITestCase):

    """Tests for REST API's delete offer view for anonymous user."""

    def test_offer_delete_status(self):
        """Test offer's delete status for anonymous user.

        API for now is read-only.
        """
        response = self.client.delete('/api/offers/1/')

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
