# -*- coding: utf-8 -*-

"""
.. module:: test_delete
"""

from rest_framework import status
from rest_framework.test import APITestCase

from apps.volontulo.tests.views.offers.commons import TestOffersCommons


class TestAdminUserOrganizationsDeleteAPIView(TestOffersCommons, APITestCase):

    """Tests for REST API's delete organization view for admin user."""

    def setUp(self):
        """Set up each test."""
        super(TestAdminUserOrganizationsDeleteAPIView, self).setUp()
        self.client.login(username='admin@example.com', password='123admin')

    def test_organization_delete_status(self):
        """Test organization's delete status for admin user.

        API for now is read-only.
        """
        response = self.client.delete('/api/organizations/1/')

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)


class TestOrganizationUserOrganizationsDeleteAPIView(
        TestOffersCommons,
        APITestCase):

    """Tests for API's delete organization view for user with organization."""

    def setUp(self):
        """Set up each test."""
        super(TestOrganizationUserOrganizationsDeleteAPIView, self).setUp()
        self.client.login(
            username='cls.organization@example.com',
            password='123org'
        )

    def test_organization_delete_status(self):
        """Test organization's delete status for user with organization.

        API for now is read-only.
        """
        response = self.client.delete('/api/organizations/1/')

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)


class TestRegularUserOrganizationsDeleteAPIView(
        TestOffersCommons,
        APITestCase):

    """Tests for REST API's delete organization view for regular user."""

    def setUp(self):
        """Set up each test."""
        super(TestRegularUserOrganizationsDeleteAPIView, self).setUp()
        self.client.login(
            username='volunteer@example.com',
            password='123volunteer'
        )

    def test_organization_delete_status(self):
        """Test organization's delete status for regular user.

        API for now is read-only.
        """
        response = self.client.delete('/api/organizations/1/')

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)


class TestAnonymousUserOrganizationsDeleteAPIView(
        TestOffersCommons,
        APITestCase):

    """Tests for REST API's delete organization view for anonymous user."""

    def test_organization_delete_status(self):
        """Test organization's delete status for anonymous user.

        API for now is read-only.
        """
        response = self.client.delete('/api/organizations/1/')

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
