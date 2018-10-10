"""
.. module:: test_delete
"""

from rest_framework import status
from rest_framework.test import APITestCase

from apps.volontulo.factories import OfferFactory
from apps.volontulo.factories import OrganizationFactory
from apps.volontulo.factories import UserFactory


class TestAdminUserOffersDeleteAPIView(APITestCase):

    """Tests for REST API's delete offer view for admin user."""

    def setUp(self):
        """Set up each test."""
        super().setUp()
        self.client.force_login(UserFactory(
            userprofile__is_administrator=True
        ))

    def test_offer_delete_status(self):
        """Test offer's delete status for admin user.

        API for now is read-only.
        """
        response = self.client.delete(
            '/api/offers/{}/'.format(OfferFactory().id)
        )
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)


class TestOrganizationUserOffersDeleteAPIView(APITestCase):

    """Tests for REST API's delete offer view for user with organization."""

    def setUp(self):
        """Set up each test."""
        super().setUp()
        self.organization = OrganizationFactory()
        self.client.force_login(UserFactory(
            userprofile__organizations=[self.organization]
        ))

    def test_offer_delete_status(self):
        """Test offer's delete status for user with organization.

        API for now is read-only.
        """
        offer = OfferFactory(organization=self.organization)
        response = self.client.delete(
            '/api/offers/{}/'.format(offer.id)
        )
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)


class TestRegularUserOffersDeleteAPIView(APITestCase):

    """Tests for REST API's delete offer view for regular user."""

    def setUp(self):
        """Set up each test."""
        super().setUp()
        self.client.force_login(UserFactory())

    def test_offer_delete_status(self):
        """Test offer's delete status for regular user.

        API for now is read-only.
        """
        response = self.client.delete(
            '/api/offers/{}/'.format(OfferFactory().id)
        )
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)


class TestAnonymousUserOffersDeleteAPIView(APITestCase):

    """Tests for REST API's delete offer view for anonymous user."""

    def test_offer_delete_status(self):
        """Test offer's delete status for anonymous user.

        API for now is read-only.
        """
        response = self.client.delete(
            '/api/offers/{}/'.format(OfferFactory().id)
        )

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
