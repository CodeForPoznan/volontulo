"""
.. module:: test_create
"""

from rest_framework import status
from rest_framework.test import APITestCase

from apps.volontulo.tests.views.offers.commons import TestOffersCommons


class _TestOffersCreateAPIView(TestOffersCommons, APITestCase):

    """Tests for REST API's create offer view."""

    def setUp(self):
        """Set up each test."""
        super(_TestOffersCreateAPIView, self).setUp()
        self.offer_payload = b"""{
            "benefits": "offer benefits",
            "description": "offer description",
            "location": "offer location",
            "organization": {"id": %d},
            "timeCommitment": "offer time commitment",
            "title": "offer title"
        }""" % self.organization.id


class TestAdminUserOffersCreateAPIView(_TestOffersCreateAPIView):

    """Tests for REST API's create offer view for admin user."""

    def setUp(self):
        """Set up each test."""
        super(TestAdminUserOffersCreateAPIView, self).setUp()
        self.client.login(username='admin@example.com', password='123admin')

    def test_offer_create_status(self):
        """Test offer's create status for admin user.

        Admin user without connected organization is not allowed to create
        offer.
        """
        response = self.client.post(
            '/api/offers/',
            self.offer_payload,
            content_type='application/json',
        )

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)


class TestOrganizationUserOffersCreateAPIView(_TestOffersCreateAPIView):

    """Tests for REST API's create offer view for user with organization."""

    def setUp(self):
        """Set up each test."""
        super(TestOrganizationUserOffersCreateAPIView, self).setUp()
        self.client.login(
            username='cls.organization@example.com',
            password='123org'
        )

    def test_offer_create_status(self):
        """Test offer's create status for user with organization.

        Regular user with connected organization is allowed to create offer for
        it.
        """
        response = self.client.post(
            '/api/offers/',
            self.offer_payload,
            content_type='application/json',
        )

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)


class TestRegularUserOffersCreateAPIView(_TestOffersCreateAPIView):

    """Tests for REST API's create offer view for regular user."""

    def setUp(self):
        """Set up each test."""
        super(TestRegularUserOffersCreateAPIView, self).setUp()
        self.client.login(
            username='volunteer@example.com',
            password='123volunteer'
        )

    def test_offer_create_status(self):
        """Test offer's create status for regular user.

        Regular user without connected organization is not allowed to create
        offer.
        """
        response = self.client.post(
            '/api/offers/',
            self.offer_payload,
            content_type='application/json',
        )

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)


class TestAnonymousUserOffersCreateAPIView(_TestOffersCreateAPIView):

    """Tests for REST API's create offer view for anonymous user."""

    def test_offer_create_status(self):
        """Test offer's create status for anonymous user.

        Anonymous user is not allowed to create offer.
        """
        response = self.client.post(
            '/api/offers/',
            self.offer_payload,
            content_type='application/json',
        )

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
