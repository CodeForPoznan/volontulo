# -*- coding: utf-8 -*-

"""
.. module:: test_read
"""

from rest_framework import status
from rest_framework.test import APITestCase

from apps.volontulo.models import Offer
from apps.volontulo.tests.views.offers.commons import TestOffersCommons


class _TestOffersReadAPIView(TestOffersCommons, APITestCase):

    """Tests for REST API's read offer view."""

    def _test_offer_read_fields(self, offer):
        """Test read's fields of offers REST API endpoint."""
        self.assertIsInstance(offer.pop('finished_at'), str)
        self.assertIsInstance(offer.pop('id'), int)
        self.assertIsInstance(offer.pop('image'), (str, type(None)))
        self.assertIsInstance(offer.pop('location'), str)
        self.assertIsInstance(offer.pop('organization'), str)
        self.assertIsInstance(offer.pop('slug'), str)
        self.assertIsInstance(offer.pop('started_at'), str)
        self.assertIsInstance(offer.pop('title'), str)
        self.assertIsInstance(offer.pop('url'), str)
        self.assertEqual(len(offer), 0)


class TestAdminUserOffersReadAPIView(_TestOffersReadAPIView):

    """Tests for REST API's read offer view for admin user."""

    def setUp(self):
        """Set up each test."""
        super(TestAdminUserOffersReadAPIView, self).setUp()
        self.client.login(username='admin@example.com', password='123admin')

    def test_offer_read_status(self):
        """Test offer's read status for admin user.

        Because we set up only 2 unpublished offers, offer will be visible only
        for admin user.
        """
        offer = Offer.objects.first()
        response = self.client.get('/api/offers/{}/'.format(offer.id))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self._test_offer_read_fields(response.data)


class TestOrganizationUserOffersReadAPIView(_TestOffersReadAPIView):

    """Tests for REST API's read offer view for user with organization."""

    def setUp(self):
        """Set up each test."""
        super(TestOrganizationUserOffersReadAPIView, self).setUp()
        self.client.login(
            username='cls.organization@example.com',
            password='123org'
        )

    def test_offer_read_status(self):
        """Test offer's read status for user with organization.

        Because we set up only 2 unpublished offers, offer will be visible only
        for admin user.
        """
        response = self.client.get('/api/offers/1/')

        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)


class TestRegularUserOffersReadAPIView(_TestOffersReadAPIView):

    """Tests for REST API's read offer view for regular user."""

    def setUp(self):
        """Set up each test."""
        super(TestRegularUserOffersReadAPIView, self).setUp()
        self.client.login(
            username='volunteer@example.com',
            password='123volunteer'
        )

    def test_offer_read_status(self):
        """Test offer's read status for regular user.

        Because we set up only 2 unpublished offers, offer will be visible only
        for admin user.
        """
        response = self.client.get('/api/offers/1/')

        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)


class TestAnonymousUserOffersReadAPIView(_TestOffersReadAPIView):

    """Tests for REST API's read offer view for anonymous user."""

    def test_offer_read_status(self):
        """Test offer's read status for anonymous user.

        Because we set up only 2 unpublished offers, offer will be visible only
        for admin user.
        """
        response = self.client.get('/api/offers/1/')

        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
