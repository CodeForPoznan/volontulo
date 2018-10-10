"""
.. module:: test_list
"""

from rest_framework import status
from rest_framework.test import APITestCase

from apps.volontulo.factories import OrganizationFactory
from apps.volontulo.factories import UserFactory


class _TestOrganizationsListAPIView(APITestCase):

    """Tests for REST API's list organizations view."""

    def test_organization_list_fields(self):
        """Test list's fields of organization REST API endpoint."""
        OrganizationFactory.create_batch(56)

        response = self.client.get('/api/organizations/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        for organization in response.data:
            self.assertIsInstance(organization.pop('address'), str)
            self.assertIsInstance(organization.pop('description'), str)
            self.assertIsInstance(organization.pop('id'), int)
            self.assertIsInstance(organization.pop('name'), str)
            self.assertIsInstance(organization.pop('slug'), str)
            self.assertIsInstance(organization.pop('url'), str)
            self.assertEqual(len(organization), 0)


class TestAdminUserOrganizationsListAPIView(_TestOrganizationsListAPIView):

    """Tests for REST API's list organizations view for admin user."""

    def setUp(self):
        """Set up each test."""
        super().setUp()
        self.client.force_login(UserFactory(
            userprofile__is_administrator=True
        ))

    def test_organization_list_length(self):
        """Test organizations list length for admin user.

        Organizations are readable for everyone.
        """
        OrganizationFactory.create_batch(61)

        response = self.client.get('/api/organizations/')

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 61)


class TestOrganizationUserOrganizationsListAPIView(
        _TestOrganizationsListAPIView):

    """Tests for API's list organizations view for user with organization."""

    def setUp(self):
        """Set up each test."""
        super().setUp()
        self.client.force_login(UserFactory(
            userprofile__organizations=[OrganizationFactory()]
        ))

    def test_organization_list_length(self):
        """Test organizations list length for user with organization.

        Organizations are readable for everyone.
        """
        OrganizationFactory.create_batch(75)

        response = self.client.get('/api/organizations/')

        self.assertEqual(response.status_code, status.HTTP_200_OK)

        # it's 76 here, as one organization is created when user is created:
        self.assertEqual(len(response.data), 76)


class TestRegularUserOrganizationsListAPIView(_TestOrganizationsListAPIView):

    """Tests for REST API's list organizations view for regular user."""

    def setUp(self):
        """Set up each test."""
        super().setUp()
        self.client.force_login(UserFactory())

    def test_organization_list_length(self):
        """Test organizations list length for regular user.

        Organizations are readable for everyone.
        """
        OrganizationFactory.create_batch(80)

        response = self.client.get('/api/organizations/')

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 80)


class TestAnonymousUserOrganizationsListAPIView(_TestOrganizationsListAPIView):

    """Tests for REST API's list organizations view for anonymous user."""

    def test_organization_list_length(self):
        """Test organizations list length for anonymous user.

        Organizations are readable for everyone.
        """
        OrganizationFactory.create_batch(93)

        response = self.client.get('/api/organizations/')

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 93)
