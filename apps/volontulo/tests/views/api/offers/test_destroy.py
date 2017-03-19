# -*- coding: utf-8 -*-

"""
.. module:: test_destroy
"""

from rest_framework import status
from rest_framework.test import APITestCase

from apps.volontulo.tests.views.offers.commons import TestOffersCommons


class TestAdminUserOffersDestroyAPIView(TestOffersCommons, APITestCase):

    """Tests for REST API's destroy offer view for admin user."""

    def setUp(self):
        """Set up each test."""
        super(TestAdminUserOffersDestroyAPIView, self).setUp()
        self.client.login(username='admin@example.com', password='123admin')

    def test_offer_destroy_status(self):
        """Test offer's destroy status for admin user.

        API for now is read-only.
        """
        response = self.client.delete('/api/offers/1/')

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)


class TestOrganizationUserOffersDestroyAPIView(TestOffersCommons, APITestCase):

    """Tests for REST API's destroy offer view for user with organization."""

    def setUp(self):
        """Set up each test."""
        super(TestOrganizationUserOffersDestroyAPIView, self).setUp()
        self.client.login(
            username='cls.organization@example.com',
            password='123org'
        )

    def test_offer_destroy_status(self):
        """Test offer's destroy status for user with organization.

        API for now is read-only.
        """
        response = self.client.delete('/api/offers/1/')

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)


class TestRegularUserOffersDestroyAPIView(TestOffersCommons, APITestCase):

    """Tests for REST API's destroy offer view for regular user."""

    def setUp(self):
        """Set up each test."""
        super(TestRegularUserOffersDestroyAPIView, self).setUp()
        self.client.login(
            username='volunteer@example.com',
            password='123volunteer'
        )

    def test_offer_destroy_status(self):
        """Test offer's destroy status for regular user.

        API for now is read-only.
        """
        response = self.client.delete('/api/offers/1/')

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)


class TestAnonymousUserOffersDestroyAPIView(TestOffersCommons, APITestCase):

    """Tests for REST API's destroy offer view for anonymous user."""

    def test_offer_update_status(self):
        """Test offer's destroy status for anonymous user.

        API for now is read-only.
        """
        response = self.client.delete('/api/offers/1/')

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
