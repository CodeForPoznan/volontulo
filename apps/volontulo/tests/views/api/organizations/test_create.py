# -*- coding: utf-8 -*-

"""
.. module:: test_create
"""

from rest_framework import status
from rest_framework.test import APITestCase

from apps.volontulo.tests.views.offers.commons import TestOffersCommons


class _TestOrganizationsCreateAPIView(TestOffersCommons, APITestCase):

    """Tests for REST API's create organization view."""

    def setUp(self):
        """Set up each test."""
        super(_TestOrganizationsCreateAPIView, self).setUp()
        self.organization_payload = (
            b'{"name": "TM",'
            b'"slug": "tm",'
            b'"url": "http://localhost:8000/api/organizations/1/"}'
        )


class TestAdminUserOrganizationsCreateAPIView(_TestOrganizationsCreateAPIView):

    """Tests for REST API's create organization view for admin user."""

    def setUp(self):
        """Set up each test."""
        super(TestAdminUserOrganizationsCreateAPIView, self).setUp()
        self.client.login(username='admin@example.com', password='123admin')

    def test_organization_create_status(self):
        """Test organization's create status for admin user.

        API for now is read-only.
        """
        response = self.client.post(
            '/api/organizations/',
            self.organization_payload,
            content_type='application/json',
        )

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)


class TestOrganizationUserOrganizationsCreateAPIView(
        _TestOrganizationsCreateAPIView):

    """Tests for REST API's create organization view for user with organization."""

    def setUp(self):
        """Set up each test."""
        super(TestOrganizationUserOrganizationsCreateAPIView, self).setUp()
        self.client.login(
            username='cls.organization@example.com',
            password='123org'
        )

    def test_organization_create_status(self):
        """Test organizations's create status for user with organization.

        API for now is read-only.
        """
        response = self.client.post(
            '/api/organizations/',
            self.organization_payload,
            content_type='application/json',
        )

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)


class TestRegularUserOrganizationsCreateAPIView(
        _TestOrganizationsCreateAPIView):

    """Tests for REST API's create organization view for regular user."""

    def setUp(self):
        """Set up each test."""
        super(TestRegularUserOrganizationsCreateAPIView, self).setUp()
        self.client.login(
            username='volunteer@example.com',
            password='123volunteer'
        )

    def test_organization_create_status(self):
        """Test organizations's create status for regular user.

        API for now is read-only.
        """
        response = self.client.post(
            '/api/organizations/',
            self.organization_payload,
            content_type='application/json',
        )

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)


class TestAnonymousUserOrganizationsCreateAPIView(
        _TestOrganizationsCreateAPIView):

    """Tests for REST API's create organization view for anonymous user."""

    def test_organization_create_status(self):
        """Test organizations's create status for anonymous user.

        API for now is read-only.
        """
        response = self.client.post(
            '/api/organizations/',
            self.organization_payload,
            content_type='application/json',
        )

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
