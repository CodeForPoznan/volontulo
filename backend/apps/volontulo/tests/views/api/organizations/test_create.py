"""
.. module:: test_create
"""

from rest_framework import status
from rest_framework.test import APITestCase

from apps.volontulo.factories import OrganizationFactory
from apps.volontulo.factories import UserFactory


class _TestOrganizationsCreateAPIView(APITestCase):

    """Tests for REST API's create organization view."""

    @classmethod
    def setUpClass(cls):
        """Set up each test."""
        super().setUpClass()
        cls.organization_payload = b"""{
            "name": "TM",
            "description": "Opis",
            "address": "ul. Koperkowa 7"
        }"""


class TestAdminUserOrganizationsCreateAPIView(_TestOrganizationsCreateAPIView):

    """Tests for REST API's create organization view for admin user."""

    def setUp(self):
        """Set up each test."""
        super().setUp()
        self.client.force_login(UserFactory(
            userprofile__is_administrator=True
        ))

    def test_organization_create_status(self):
        """Test organization's create status for admin user.

        API for now is read-only.
        """
        response = self.client.post(
            '/api/organizations/',
            self.organization_payload,
            content_type='application/json',
        )

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)


class TestOrganizationUserOrganizationsCreateAPIView(
        _TestOrganizationsCreateAPIView):

    """Tests for API's create organization view for user with organization."""

    def setUp(self):
        """Set up each test."""
        super().setUp()
        self.client.force_login(UserFactory(
            userprofile__organizations=[OrganizationFactory()]
        ))

    def test_organization_create_status(self):
        """Test organization create status for user with organization.

        API for now is read-only.
        """
        response = self.client.post(
            '/api/organizations/',
            self.organization_payload,
            content_type='application/json',
        )

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)


class TestRegularUserOrganizationsCreateAPIView(
        _TestOrganizationsCreateAPIView):

    """Tests for REST API's create organization view for regular user."""

    def setUp(self):
        """Set up each test."""
        super().setUp()
        self.client.force_login(UserFactory())

    def test_organization_create_status(self):
        """Test organization create status for regular user.

        API for now is read-only.
        """
        response = self.client.post(
            '/api/organizations/',
            self.organization_payload,
            content_type='application/json',
        )

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)


class TestAnonymousUserOrganizationsCreateAPIView(
        _TestOrganizationsCreateAPIView):

    """Tests for REST API's create organization view for anonymous user."""

    def test_organization_create_status(self):
        """Test organization create status for anonymous user.

        API for now is read-only.
        """
        response = self.client.post(
            '/api/organizations/',
            self.organization_payload,
            content_type='application/json',
        )

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
