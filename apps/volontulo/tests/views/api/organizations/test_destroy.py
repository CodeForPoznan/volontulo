# -*- coding: utf-8 -*-

"""
.. module:: test_destroy
"""

from rest_framework import status
from rest_framework.test import APITestCase

from apps.volontulo.tests.views.offers.commons import TestOffersCommons


class TestAdminUserOrganizationsDestroyAPIView(TestOffersCommons, APITestCase):

    """Tests for REST API's destroy organization view for admin user."""

    def setUp(self):
        """Set up each test."""
        super(TestAdminUserOrganizationsDestroyAPIView, self).setUp()
        self.client.login(username='admin@example.com', password='123admin')

    def test_organization_destroy_status(self):
        """Test organization's destroy status for admin user.

        API for now is read-only.
        """
        response = self.client.delete('/api/organizations/1/')

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)


class TestOrganizationUserOrganizationsDestroyAPIView(
        TestOffersCommons,
        APITestCase):

    """Tests for API's destroy organization view for user with organization."""

    def setUp(self):
        """Set up each test."""
        super(TestOrganizationUserOrganizationsDestroyAPIView, self).setUp()
        self.client.login(
            username='cls.organization@example.com',
            password='123org'
        )

    def test_organization_destroy_status(self):
        """Test organization's destroy status for user with organization.

        API for now is read-only.
        """
        response = self.client.delete('/api/organizations/1/')

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)


class TestRegularUserOrganizationsDestroyAPIView(
        TestOffersCommons,
        APITestCase):

    """Tests for REST API's destroy organization view for regular user."""

    def setUp(self):
        """Set up each test."""
        super(TestRegularUserOrganizationsDestroyAPIView, self).setUp()
        self.client.login(
            username='volunteer@example.com',
            password='123volunteer'
        )

    def test_organization_destroy_status(self):
        """Test organization's destroy status for regular user.

        API for now is read-only.
        """
        response = self.client.delete('/api/organizations/1/')

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)


class TestAnonymousUserOrganizationsDestroyAPIView(
        TestOffersCommons,
        APITestCase):

    """Tests for REST API's destroy organization view for anonymous user."""

    def test_organization_update_status(self):
        """Test organization's destroy status for anonymous user.

        API for now is read-only.
        """
        response = self.client.delete('/api/organizations/1/')

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
