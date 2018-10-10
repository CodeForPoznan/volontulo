"""
.. module:: test_update
"""

from rest_framework import status
from rest_framework.test import APITestCase

from apps.volontulo.factories import OrganizationFactory
from apps.volontulo.factories import UserFactory


class _TestOrganizationsUpdateAPIView(APITestCase):

    """Tests for REST API's update organization view."""

    @classmethod
    def setUpClass(cls):
        """Set up test case."""
        super().setUpClass()
        cls.organization_payload = b"""{
            "name": "TM",
            "description": "Opis",
            "address": "ul. Koperkowa 7"
        }"""


class TestAdminUserOrganizationsUpdateAPIView(_TestOrganizationsUpdateAPIView):

    """Tests for REST API's update organization view for admin user."""

    def setUp(self):
        """Set up each test."""
        super().setUp()
        self.client.force_login(UserFactory(
            userprofile__is_administrator=True
        ))

    def test_organization_update_status(self):
        """Test organization's update status for admin user.

        API for now is read-only.
        """
        response = self.client.put(
            '/api/organizations/{}/'.format(OrganizationFactory().id),
            self.organization_payload,
            content_type='application/json',
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK)


class TestOrganizationUserOrganizationsUpdateAPIView(
        _TestOrganizationsUpdateAPIView):

    """Tests for API's update organization view for user with organization."""

    def setUp(self):
        """Set up each test."""
        super().setUp()
        self.organization = OrganizationFactory()
        self.client.force_login(UserFactory(
            userprofile__organizations=[self.organization]
        ))

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
        super().setUp()
        self.client.force_login(UserFactory())

    def test_organization_update_status(self):
        """Test organization's update status for regular user.

        API for now is read-only.
        """
        self.client.force_login(UserFactory())

        response = self.client.put(
            '/api/organizations/{}/'.format(OrganizationFactory().id),
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
            '/api/organizations/{}/'.format(OrganizationFactory().id),
            self.organization_payload,
            content_type='application/json',
        )

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
