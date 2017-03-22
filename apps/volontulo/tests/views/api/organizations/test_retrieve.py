# -*- coding: utf-8 -*-

"""
.. module:: test_retrieve
"""

from rest_framework import status
from rest_framework.test import APITestCase

from apps.volontulo.models import Organization
from apps.volontulo.tests.views.offers.commons import TestOffersCommons


class _TestOrganizationsRetrieveAPIView(TestOffersCommons, APITestCase):

    """Tests for REST API's retrieve organization view."""

    def _test_organization_retrieve_fields(self, organization):
        """Test retrieve's fields of organizations REST API endpoint."""
        self.assertIsInstance(organization.pop('id'), int)
        self.assertIsInstance(organization.pop('name'), str)
        self.assertIsInstance(organization.pop('slug'), str)
        self.assertIsInstance(organization.pop('url'), str)
        self.assertEqual(len(organization), 0)


class TestAdminUserOrganizationsRetrieveAPIView(
        _TestOrganizationsRetrieveAPIView):

    """Tests for REST API's retrieve organization view for admin user."""

    def setUp(self):
        """Set up each test."""
        super(TestAdminUserOrganizationsRetrieveAPIView, self).setUp()
        self.client.login(username='admin@example.com', password='123admin')

    def test_organization_retrieve_status(self):
        """Test organization's retrieve status for admin user.

        Organizations are readable for everyone.
        """
        organization = Organization.objects.first()
        response = self.client.get(
            '/api/organizations/{}/'.format(organization.id))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self._test_organization_retrieve_fields(response.data)


class TestOrganizationUserOrganizationsRetrieveAPIView(
        _TestOrganizationsRetrieveAPIView):

    """Tests for API's retrieve organization view for user with organization."""

    def setUp(self):
        """Set up each test."""
        super(TestOrganizationUserOrganizationsRetrieveAPIView, self).setUp()
        self.client.login(
            username='cls.organization@example.com',
            password='123org'
        )

    def test_organization_retrieve_status(self):
        """Test organization's retrieve status for user with organization.

        Organizations are readable for everyone.
        """
        organization = Organization.objects.first()
        response = self.client.get(
            '/api/organizations/{}/'.format(organization.id))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self._test_organization_retrieve_fields(response.data)


class TestRegularUserOrganizationsRetrieveAPIView(
        _TestOrganizationsRetrieveAPIView):

    """Tests for REST API's retrieve organization view for regular user."""

    def setUp(self):
        """Set up each test."""
        super(TestRegularUserOrganizationsRetrieveAPIView, self).setUp()
        self.client.login(
            username='volunteer@example.com',
            password='123volunteer'
        )

    def test_organization_retrieve_status(self):
        """Test organization's retrieve status for regular user.

        Organizations are readable for everyone.
        """
        organization = Organization.objects.first()
        response = self.client.get(
            '/api/organizations/{}/'.format(organization.id))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self._test_organization_retrieve_fields(response.data)


class TestAnonymousUserOrganizationsRetrieveAPIView(
        _TestOrganizationsRetrieveAPIView):

    """Tests for REST API's retrieve organization view for anonymous user."""

    def test_organization_retrieve_status(self):
        """Test organization's retrieve status for anonymous user.

        Organizations are readable for everyone.
        """
        organization = Organization.objects.first()
        response = self.client.get(
            '/api/organizations/{}/'.format(organization.id))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self._test_organization_retrieve_fields(response.data)
