# -*- coding: utf-8 -*-

"""
.. module:: test_update
"""

from rest_framework import status
from rest_framework.test import APITestCase

from apps.volontulo.tests.views.offers.commons import TestOffersCommons


class _TestOrganizationsUpdateAPIView(TestOffersCommons, APITestCase):

    """Tests for REST API's update organization view."""

    def setUp(self):
        """Set up each test."""
        super(_TestOrganizationsUpdateAPIView, self).setUp()
        self.organization_payload = b"""{
            "name": "TM",
            "description": "Opis",
            "address": "ul. Koperkowa 7"
        }"""


class TestAdminUserOrganizationsUpdateAPIView(_TestOrganizationsUpdateAPIView):

    """Tests for REST API's update organization view for admin user."""

    def setUp(self):
        """Set up each test."""
        super(TestAdminUserOrganizationsUpdateAPIView, self).setUp()
        self.client.login(username='admin@example.com', password='123admin')

    def test_organization_update_status(self):
        """Test organization's update status for admin user.

        API for now is read-only.
        """
        response = self.client.put(
            '/api/organizations/{}/'.format(self.organization.id),
            self.organization_payload,
            content_type='application/json',
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK)


class TestOrganizationUserOrganizationsUpdateAPIView(
        _TestOrganizationsUpdateAPIView):

    """Tests for API's update organization view for user with organization."""

    def setUp(self):
        """Set up each test."""
        super(TestOrganizationUserOrganizationsUpdateAPIView, self).setUp()
        self.client.login(
            username='cls.organization@example.com',
            password='123org'
        )

    def test_organization_update_status(self):
        """Test organization's update status for user with organization.

        API for now is read-only.
        """
        response = self.client.put(
            '/api/organizations/{}/'.format(self.organization.id),
            self.organization_payload,
            content_type='application/json',
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)


class TestRegularUserOrganizationsUpdateAPIView(
        _TestOrganizationsUpdateAPIView):

    """Tests for REST API's update organization view for regular user."""

    def setUp(self):
        """Set up each test."""
        super(TestRegularUserOrganizationsUpdateAPIView, self).setUp()
        self.client.login(
            username='volunteer@example.com',
            password='123volunteer'
        )

    def test_organization_update_status(self):
        """Test organization's update status for regular user.

        API for now is read-only.
        """
        response = self.client.put(
            '/api/organizations/{}/'.format(self.organization.id),
            self.organization_payload,
            content_type='application/json',
        )
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)


class TestAnonymousUserOrganizationsUpdateAPIView(
        _TestOrganizationsUpdateAPIView):

    """Tests for REST API's update organization view for anonymous user."""

    def test_organization_update_status(self):
        """Test organization's update status for anonymous user.

        API for now is read-only.
        """
        response = self.client.put(
            '/api/organizations/{}/'.format(self.organization.id),
            self.organization_payload,
            content_type='application/json',
        )

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
