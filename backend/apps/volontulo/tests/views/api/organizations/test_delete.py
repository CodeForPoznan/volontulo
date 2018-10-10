"""
.. module:: test_delete
"""

from rest_framework import status
from rest_framework.test import APITestCase

from apps.volontulo.factories import OrganizationFactory
from apps.volontulo.factories import UserFactory


class TestAdminUserOrganizationsDeleteAPIView(APITestCase):

    """Tests for REST API's delete organization view for admin user."""

    def setUp(self):
        """Set up each test."""
        super().setUp()
        self.client.force_login(UserFactory(
            userprofile__is_administrator=True
        ))

    def test_organization_delete_status(self):
        """Test organization's delete status for admin user.

        API for now is read-only.
        """
        response = self.client.delete(
            '/api/organizations/{}/'.format(OrganizationFactory())
        )

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)


class TestOrganizationUserOrganizationsDeleteAPIView(APITestCase):

    """Tests for API's delete organization view for user with organization."""

    def setUp(self):
        """Set up each test."""
        super().setUp()
        self.client.force_login(UserFactory(
            userprofile__organizations=[OrganizationFactory()]
        ))

    def test_organization_delete_status(self):
        """Test organization's delete status for user with organization.

        API for now is read-only.
        """
        response = self.client.delete(
            '/api/organizations/{}/'.format(OrganizationFactory())
        )

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)


class TestRegularUserOrganizationsDeleteAPIView(APITestCase):

    """Tests for REST API's delete organization view for regular user."""

    def setUp(self):
        """Set up each test."""
        super().setUp()
        self.client.force_login(UserFactory())

    def test_organization_delete_status(self):
        """Test organization's delete status for regular user.

        API for now is read-only.
        """
        response = self.client.delete(
            '/api/organizations/{}/'.format(OrganizationFactory())
        )

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)


class TestAnonymousUserOrganizationsDeleteAPIView(APITestCase):

    """Tests for REST API's delete organization view for anonymous user."""

    def test_organization_delete_status(self):
        """Test organization's delete status for anonymous user.

        API for now is read-only.
        """
        response = self.client.delete(
            '/api/organizations/{}/'.format(OrganizationFactory())
        )

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
