"""
.. module:: test_read
"""

from rest_framework import status
from rest_framework.test import APITestCase

from apps.volontulo.factories import OrganizationFactory
from apps.volontulo.factories import UserFactory


class _TestOrganizationsReadAPIView(APITestCase):

    """Tests for REST API's read organization view."""

    def _test_organization_read_fields(self, organization):
        """Test read's fields of organizations REST API endpoint."""
        self.assertIsInstance(organization.pop('address'), str)
        self.assertIsInstance(organization.pop('description'), str)
        self.assertIsInstance(organization.pop('id'), int)
        self.assertIsInstance(organization.pop('name'), str)
        self.assertIsInstance(organization.pop('slug'), str)
        self.assertIsInstance(organization.pop('url'), str)
        self.assertEqual(len(organization), 0)


class TestAdminUserOrganizationsReadAPIView(_TestOrganizationsReadAPIView):

    """Tests for REST API's read organization view for admin user."""

    def setUp(self):
        """Set up each test."""
        super().setUp()
        self.client.force_login(UserFactory(
            userprofile__is_administrator=True
        ))

    def test_organization_read_status(self):
        """Test organization's read status for admin user.

        Organizations are readable for everyone.
        """
        response = self.client.get(
            '/api/organizations/{id}/'.format(id=OrganizationFactory().id))

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self._test_organization_read_fields(response.data)


class TestOrganizationUserOrganizationsReadAPIView(
        _TestOrganizationsReadAPIView):

    """Tests for API's read organization view for user with organization."""

    def setUp(self):
        """Set up each test."""
        super().setUp()
        self.client.force_login(UserFactory(
            userprofile__organizations=[OrganizationFactory()]
        ))

    def test_organization_read_status(self):
        """Test organization's read status for user with organization.

        Organizations are readable for everyone.
        """
        response = self.client.get(
            '/api/organizations/{id}/'.format(id=OrganizationFactory().id))

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self._test_organization_read_fields(response.data)


class TestRegularUserOrganizationsReadAPIView(_TestOrganizationsReadAPIView):

    """Tests for REST API's read organization view for regular user."""

    def setUp(self):
        """Set up each test."""
        super().setUp()
        self.client.force_login(UserFactory())

    def test_organization_read_status(self):
        """Test organization's read status for regular user.

        Organizations are readable for everyone.
        """
        self.client.force_login(UserFactory())

        response = self.client.get(
            '/api/organizations/{id}/'.format(id=OrganizationFactory().id))

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self._test_organization_read_fields(response.data)


class TestAnonymousUserOrganizationsReadAPIView(_TestOrganizationsReadAPIView):

    """Tests for REST API's read organization view for anonymous user."""

    def test_organization_read_status(self):
        """Test organization's read status for anonymous user.

        Organizations are readable for everyone.
        """
        response = self.client.get(
            '/api/organizations/{id}/'.format(id=OrganizationFactory().id))

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self._test_organization_read_fields(response.data)
