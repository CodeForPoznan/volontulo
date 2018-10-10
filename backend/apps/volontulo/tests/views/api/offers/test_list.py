"""
.. module:: test_list
"""

from rest_framework import status
from rest_framework.test import APITestCase

from apps.volontulo.factories import OfferFactory
from apps.volontulo.factories import OrganizationFactory
from apps.volontulo.factories import UserFactory
from apps.volontulo.tests import common


class _TestOffersListAPIView(APITestCase):

    """Tests for REST API's list offers view."""

    def test_offer_list_fields(self):
        """Test list's fields of offers REST API endpoint."""
        OfferFactory.create_batch(42)

        response = self.client.get('/api/offers/')

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        for offer in response.data:
            common.test_offer_list_fields(self, offer)


class TestAdminUserOffersListAPIView(_TestOffersListAPIView):

    """Tests for REST API's list offers view for admin user."""

    def setUp(self):
        """Set up each test."""
        super().setUp()
        self.client.force_login(UserFactory(
            userprofile__is_administrator=True
        ))

    def test_offer_list_length(self):
        """Test offers list length for admin user.

        All existing offers are visible for admin user.
        """
        OfferFactory.create_batch(42)

        response = self.client.get('/api/offers/')

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 42)


class TestOrganizationUserOffersListAPIView(_TestOffersListAPIView):

    """Tests for REST API's list offers view for user with organization."""

    def setUp(self):
        """Set up each test."""
        super().setUp()
        self.organization = OrganizationFactory()
        self.client.force_login(UserFactory(
            userprofile__organizations=[self.organization]
        ))

    def test_offer_list_length(self):
        """Test offers list length for user with organization.

        Because we set up 74 unpublished offer create for user's organization
        and 21 published, user with organization will see 95 offers.
        """
        OfferFactory.create_batch(21, offer_status='published')
        OfferFactory.create_batch(37, offer_status='unpublished')
        OfferFactory.create_batch(42, offer_status='rejected')
        OfferFactory.create_batch(74, organization=self.organization)

        response = self.client.get('/api/offers/')

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 95)


class TestRegularUserOffersListAPIView(_TestOffersListAPIView):

    """Tests for REST API's list offers view for regular user."""

    def setUp(self):
        """Set up each test."""
        super().setUp()
        self.client.force_login(UserFactory())

    def test_offer_list_length(self):
        """Test offers list length for regular user.

        Because we set up 34 published offers, only them  will be visible for
        regular user.
        """
        OfferFactory.create_batch(34, offer_status='published')
        OfferFactory.create_batch(73, offer_status='unpublished')
        OfferFactory.create_batch(37, offer_status='rejected')

        response = self.client.get('/api/offers/')

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 34)


class TestAnonymousUserOffersListAPIView(_TestOffersListAPIView):

    """Tests for REST API's list offers view for anonymous user."""

    def test_offer_list_length(self):
        """Test offers list length for anonymous user.

        Because we set up 13 published offers, only them will be visible for
        anonymous user.
        """
        OfferFactory.create_batch(13, offer_status='published')
        OfferFactory.create_batch(54, offer_status='unpublished')
        OfferFactory.create_batch(47, offer_status='rejected')

        response = self.client.get('/api/offers/')

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 13)
