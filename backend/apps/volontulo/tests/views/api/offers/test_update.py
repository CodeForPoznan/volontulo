"""
.. module:: test_update
"""

from rest_framework import status
from rest_framework.test import APITestCase

from apps.volontulo.tests.views.offers.commons import TestOffersCommons


class _TestOffersUpdateAPIView(TestOffersCommons, APITestCase):

    """Tests for REST API's update offer view."""

    def setUp(self):
        """Set up each test."""
        super(_TestOffersUpdateAPIView, self).setUp()
        self.offer_payload = b"""{
            "benefits": "offer benefits",
            "description": "offer description",
            "location": "offer location",
            "organization": {"id": %d},
            "timeCommitment": "offer time commitment",
            "title": "offer title"
        }""" % self.organization.id


class TestAdminUserOffersUpdateAPIView(_TestOffersUpdateAPIView):

    """Tests for REST API's update offer view for admin user."""

    def setUp(self):
        """Set up each test."""
        super(TestAdminUserOffersUpdateAPIView, self).setUp()
        self.client.login(username='admin@example.com', password='123admin')

    def test_offer_update_status(self):
        """Test offer's update status for admin user.

        Admin user without connected organization is allowed to edit any offer.
        """
        response = self.client.put(
            '/api/offers/{}/'.format(self.active_offer.id),
            self.offer_payload,
            content_type='application/json',
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK)


class TestOrganizationUserOffersUpdateAPIView(_TestOffersUpdateAPIView):

    """Tests for REST API's update offer view for user with organization."""

    def setUp(self):
        """Set up each test."""
        super(TestOrganizationUserOffersUpdateAPIView, self).setUp()
        self.client.login(
            username='cls.organization@example.com',
            password='123org'
        )

    def test_offer_update_status(self):
        """Test offer's update status for user with organization.

        Regular user with connected organization is allowed to edit its offer.
        """
        response = self.client.put(
            '/api/offers/{}/'.format(self.active_offer.id),
            self.offer_payload,
            content_type='application/json',
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK)


class TestRegularUserOffersUpdateAPIView(_TestOffersUpdateAPIView):

    """Tests for REST API's update offer view for regular user."""

    def setUp(self):
        """Set up each test."""
        super(TestRegularUserOffersUpdateAPIView, self).setUp()
        self.client.login(
            username='volunteer@example.com',
            password='123volunteer'
        )

    def test_offer_update_status(self):
        """Test offer's update status for regular user.

        Regular user without connected organization is not allowed to edit
        offer.
        """
        response = self.client.put(
            '/api/offers/{}/'.format(self.active_offer.id),
            self.offer_payload,
            content_type='application/json',
        )

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)


class TestAnonymousUserOffersUpdateAPIView(_TestOffersUpdateAPIView):

    """Tests for REST API's update offer view for anonymous user."""

    def test_offer_update_status(self):
        """Test offer's update status for anonymous user.

        Anonymous user is not allowed to edit offer.
        """
        response = self.client.put(
            '/api/offers/{}/'.format(self.active_offer.id),
            self.offer_payload,
            content_type='application/json',
        )

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
