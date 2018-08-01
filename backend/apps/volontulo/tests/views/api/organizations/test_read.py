# -*- coding: utf-8 -*-

"""
.. module:: test_read
"""

from rest_framework import status
from rest_framework.test import APITestCase

from apps.volontulo.models import Organization
from apps.volontulo.tests.views.offers.commons import TestOffersCommons


class _TestOrganizationsReadAPIView(TestOffersCommons, APITestCase):

    """Tests for REST API's read organization view."""

    def _test_organization_read_fields(self, organization):
        """Test read's fields of organizations REST API endpoint."""
        self.assertIsInstance(organization.pop('address'), str)
        self.assertIsInstance(organization.pop('description'), str)
        self.assertIsInstance(organization.pop('id'), int)
        self.assertIsInstance(organization.pop('name'), str)
        self.assertIsInstance(organization.pop('slug'), str)
        self.assertEqual(len(organization), 0)


class TestAdminUserOrganizationsReadAPIView(_TestOrganizationsReadAPIView):

    """Tests for REST API's read organization view for admin user."""

    def setUp(self):
        """Set up each test."""
        super(TestAdminUserOrganizationsReadAPIView, self).setUp()
        self.client.login(username='admin@example.com', password='123admin')

    def test_organization_read_status(self):
        """Test organization's read status for admin user.

        Organizations are readable for everyone.
        """
        organization = Organization.objects.first()
        response = self.client.get(
            '/api/organizations/{id}/'.format(id=organization.id))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self._test_organization_read_fields(response.data)


class TestOrganizationUserOrganizationsReadAPIView(
        _TestOrganizationsReadAPIView):

    """Tests for API's read organization view for user with organization."""

    def setUp(self):
        """Set up each test."""
        super(TestOrganizationUserOrganizationsReadAPIView, self).setUp()
        self.client.login(
            username='cls.organization@example.com',
            password='123org'
        )

    def test_organization_read_status(self):
        """Test organization's read status for user with organization.

        Organizations are readable for everyone.
        """
        organization = Organization.objects.first()
        response = self.client.get(
            '/api/organizations/{id}/'.format(id=organization.id))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self._test_organization_read_fields(response.data)


class TestRegularUserOrganizationsReadAPIView(_TestOrganizationsReadAPIView):

    """Tests for REST API's read organization view for regular user."""

    def setUp(self):
        """Set up each test."""
        super(TestRegularUserOrganizationsReadAPIView, self).setUp()
        self.client.login(
            username='volunteer@example.com',
            password='123volunteer'
        )

    def test_organization_read_status(self):
        """Test organization's read status for regular user.

        Organizations are readable for everyone.
        """
        organization = Organization.objects.first()
        response = self.client.get(
            '/api/organizations/{id}/'.format(id=organization.id))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self._test_organization_read_fields(response.data)


class TestAnonymousUserOrganizationsReadAPIView(_TestOrganizationsReadAPIView):

    """Tests for REST API's read organization view for anonymous user."""

    def test_organization_read_status(self):
        """Test organization's read status for anonymous user.

        Organizations are readable for everyone.
        """
        organization = Organization.objects.first()
        response = self.client.get(
            '/api/organizations/{id}/'.format(id=organization.id))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self._test_organization_read_fields(response.data)
