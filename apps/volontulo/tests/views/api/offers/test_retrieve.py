# -*- coding: utf-8 -*-

"""
.. module:: test_retrieve
"""

from io import BytesIO

from rest_framework import status
from rest_framework.test import APITestCase
from djangorestframework_camel_case.parser import CamelCaseJSONParser

from apps.volontulo.models import Offer
from apps.volontulo.tests.views.offers.commons import TestOffersCommons


class _TestOffersRetrieveAPIView(TestOffersCommons, APITestCase):

    """Tests for REST API's retrieve offer view."""

    def _test_offer_retrieve_fields(self, offer):
        """Test retrieve's fields of offers REST API endpoint."""
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


class TestAdminUserOffersRetrieveAPIView(_TestOffersRetrieveAPIView):

    """Tests for REST API's retrieve offer view for admin user."""

    def setUp(self):
        """Set up each test."""
        super(TestAdminUserOffersRetrieveAPIView, self).setUp()
        self.client.login(username='admin@example.com', password='123admin')

    def test_offer_retrieve_status(self):
        """Test offer's retrieve status for admin user.

        Because we set up only 2 unpublished offers, offer will be visible only
        for admin user.
        """
        offer = Offer.objects.first()
        response = self.client.get('/api/offers/{}/'.format(offer.id))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self._test_offer_retrieve_fields(
            CamelCaseJSONParser().parse(BytesIO(response.content)))


class TestOrganizationUserOffersRetrieveAPIView(_TestOffersRetrieveAPIView):

    """Tests for REST API's retrieve offer view for user with organization."""

    def setUp(self):
        """Set up each test."""
        super(TestOrganizationUserOffersRetrieveAPIView, self).setUp()
        self.client.login(
            username='cls.organization@example.com',
            password='123org'
        )

    def test_offer_retrieve_status(self):
        """Test offer's retrieve status for user with organization.

        Because we set up only 2 unpublished offers, offer will be visible only
        for admin user.
        """
        response = self.client.get('/api/offers/1/')

        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)


class TestRegularUserOffersRetrieveAPIView(_TestOffersRetrieveAPIView):

    """Tests for REST API's retrieve offer view for regular user."""

    def setUp(self):
        """Set up each test."""
        super(TestRegularUserOffersRetrieveAPIView, self).setUp()
        self.client.login(
            username='volunteer@example.com',
            password='123volunteer'
        )

    def test_offer_retrieve_status(self):
        """Test offer's retrieve status for regular user.

        Because we set up only 2 unpublished offers, offer will be visible only
        for admin user.
        """
        response = self.client.get('/api/offers/1/')

        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)


class TestAnonymousUserOffersRetrieveAPIView(_TestOffersRetrieveAPIView):

    """Tests for REST API's retrieve offer view for anonymous user."""

    def test_offer_retrieve_status(self):
        """Test offer's retrieve status for anonymous user.

        Because we set up only 2 unpublished offers, offer will be visible only
        for admin user.
        """
        response = self.client.get('/api/offers/1/')

        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
