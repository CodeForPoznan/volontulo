# -*- coding: utf-8 -*-

"""
.. module:: test_list
"""

from io import BytesIO

from rest_framework import status
from rest_framework.test import APITestCase
from djangorestframework_camel_case.parser import CamelCaseJSONParser

from apps.volontulo.tests.views.offers.commons import TestOffersCommons


class _TestOffersListAPIView(TestOffersCommons, APITestCase):

    """Tests for REST API's list offers view."""

    def test_offer_list_fields(self):
        """Test list's fields of offers REST API endpoint."""
        response = self.client.get('/api/offers/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        # dirty hack intead of checking response.data because of issue
        # djangorestframework-camel-case #26:
        for offer in CamelCaseJSONParser().parse(BytesIO(response.content)):
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


class TestAdminUserOffersListAPIView(_TestOffersListAPIView):

    """Tests for REST API's list offers view for admin user."""

    def setUp(self):
        """Set up each test."""
        super(TestAdminUserOffersListAPIView, self).setUp()
        self.client.login(username='admin@example.com', password='123admin')

    def test_offer_list_length(self):
        """Test offers list length for admin user.

        Because we set up only 2 unpublished offers, they will be visible only
        for admin user.
        """
        response = self.client.get('/api/offers/')

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 2)


class TestOrganizationUserOffersListAPIView(_TestOffersListAPIView):

    """Tests for REST API's list offers view for user with organization."""

    def setUp(self):
        """Set up each test."""
        super(TestOrganizationUserOffersListAPIView, self).setUp()
        self.client.login(
            username='cls.organization@example.com',
            password='123org'
        )

    def test_offer_list_length(self):
        """Test offers list length for user with organization.

        Because we set up only 2 unpublished offers, they will be visible only
        for admin user.
        """
        response = self.client.get('/api/offers/')

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 0)


class TestRegularUserOffersListAPIView(_TestOffersListAPIView):

    """Tests for REST API's list offers view for regular user."""

    def setUp(self):
        """Set up each test."""
        super(TestRegularUserOffersListAPIView, self).setUp()
        self.client.login(
            username='volunteer@example.com',
            password='123volunteer'
        )

    def test_offer_list_length(self):
        """Test offers list length for regular user.

        Because we set up only 2 unpublished offers, they will be visible only
        for admin user.
        """
        response = self.client.get('/api/offers/')

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 0)


class TestAnonymousUserOffersListAPIView(_TestOffersListAPIView):

    """Tests for REST API's list offers view for anonymous user."""

    def test_offer_list_length(self):
        """Test offers list length for anonymous user.

        Because we set up only 2 unpublished offers, they will be visible only
        for admin user.
        """
        response = self.client.get('/api/offers/')

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 0)
