# -*- coding: utf-8 -*-

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
        self.offer_payload = (
            b'{"finishedAt":"2105-11-28T12:13:14Z",'
            b'"image":null,'
            b'"location":"",'
            b'"organization":"http://testserver/api/organizations/1/",'
            b'"slug":"volontulo-offer",'
            b'"startedAt":"2105-10-24T09:10:11Z",'
            b'"title":"volontulo offer",'
            b'"url":"http://testserver/api/offers/1/"}'
        )


class TestAdminUserOffersUpdateAPIView(_TestOffersUpdateAPIView):

    """Tests for REST API's update offer view for admin user."""

    def setUp(self):
        """Set up each test."""
        super(TestAdminUserOffersUpdateAPIView, self).setUp()
        self.client.login(username='admin@example.com', password='123admin')

    def test_offer_update_status(self):
        """Test offer's update status for admin user.

        API for now is read-only.
        """
        response = self.client.put(
            '/api/offers/1/',
            self.offer_payload,
            content_type='application/json',
        )

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)


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

        API for now is read-only.
        """
        response = self.client.put(
            '/api/offers/1/',
            self.offer_payload,
            content_type='application/json',
        )

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)


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

        API for now is read-only.
        """
        response = self.client.put(
            '/api/offers/1/',
            self.offer_payload,
            content_type='application/json',
        )

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)


class TestAnonymousUserOffersUpdateAPIView(_TestOffersUpdateAPIView):

    """Tests for REST API's update offer view for anonymous user."""

    def test_offer_update_status(self):
        """Test offer's update status for anonymous user.

        API for now is read-only.
        """
        response = self.client.put(
            '/api/offers/1/',
            self.offer_payload,
            content_type='application/json',
        )

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
