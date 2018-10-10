"""
.. module:: test_update
"""

from rest_framework import status
from rest_framework.test import APITestCase

from apps.volontulo.factories import OfferFactory
from apps.volontulo.factories import OrganizationFactory
from apps.volontulo.factories import UserFactory


class _TestOffersUpdateAPIView(APITestCase):

    """Tests for REST API's update offer view."""

    @classmethod
    def setUpClass(cls):
        """Set up each test."""
        super().setUpClass()
        cls.organization = OrganizationFactory()
        cls.offer_payload = b"""{
            "benefits": "offer benefits",
            "description": "offer description",
            "location": "offer location",
            "organization": {"id": %d},
            "timeCommitment": "offer time commitment",
            "title": "offer title"
        }""" % cls.organization.id


class TestAdminUserOffersUpdateAPIView(_TestOffersUpdateAPIView):

    """Tests for REST API's update offer view for admin user."""

    def setUp(self):
        """Set up each test."""
        super().setUp()
        self.client.force_login(UserFactory(
            userprofile__is_administrator=True
        ))

    def test_offer_update_status(self):
        """Test offer's update status for admin user.

        Admin user without connected organization is allowed to edit any offer.
        """
        response = self.client.put(
            '/api/offers/{}/'.format(OfferFactory().id),
            self.offer_payload,
            content_type='application/json',
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK)


class TestOrganizationUserOffersUpdateAPIView(_TestOffersUpdateAPIView):

    """Tests for REST API's update offer view for user with organization."""

    def setUp(self):
        """Set up each test."""
        super().setUp()
        self.client.force_login(UserFactory(
            userprofile__organizations=[self.organization]
        ))

    def test_offer_update_status(self):
        """Test offer's update status for user with organization.

        Regular user with connected organization is allowed to edit its offer.
        """
        self.client.force_login(UserFactory(
            userprofile__organizations=[self.organization]
        ))

        response = self.client.put(
            '/api/offers/{}/'.format(
                OfferFactory(organization=self.organization).id
            ),
            self.offer_payload,
            content_type='application/json'
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK)


class TestRegularUserOffersUpdateAPIView(_TestOffersUpdateAPIView):

    """Tests for REST API's update offer view for regular user."""

    def setUp(self):
        """Set up each test."""
        super().setUp()
        self.client.force_login(UserFactory())

    def test_offer_update_status(self):
        """Test offer's update status for regular user.

        Regular user without connected organization is not allowed to edit
        offer.
        """
        self.client.force_login(UserFactory())

        response = self.client.put('/api/offers/{}/'.format(
            OfferFactory(offer_status='published').id
        ), self.offer_payload, content_type='application/json')

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)


class TestAnonymousUserOffersUpdateAPIView(_TestOffersUpdateAPIView):

    """Tests for REST API's update offer view for anonymous user."""

    def test_offer_update_status(self):
        """Test offer's update status for anonymous user.

        Anonymous user is not allowed to edit offer.
        """
        response = self.client.put('/api/offers/{}/'.format(
            OfferFactory(offer_status='published').id
        ), self.offer_payload, content_type='application/json',)

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
