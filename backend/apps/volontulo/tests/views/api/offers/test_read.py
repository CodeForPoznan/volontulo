"""
.. module:: test_read
"""

from rest_framework import status
from rest_framework.test import APITestCase

from apps.volontulo.factories import OfferFactory
from apps.volontulo.factories import OrganizationFactory
from apps.volontulo.factories import UserFactory
from apps.volontulo.tests import common


class TestAdminUserOffersReadAPIView(APITestCase):

    """Tests for REST API's read offer view for admin user."""

    def setUp(self):
        """Set up each test."""
        super().setUp()
        self.client.force_login(UserFactory(
            userprofile__is_administrator=True
        ))

    def test_offer_read_status(self):
        """Test offer's read status for admin user.

        All existing offers are visible for admin user.
        """
        for offer in OfferFactory.create_batch(63):
            response = self.client.get('/api/offers/{id}/'.format(id=offer.id))
            self.assertEqual(response.status_code, status.HTTP_200_OK)
            common.test_offer_list_fields(self, response.data)


class TestOrganizationUserOffersReadAPIView(APITestCase):

    """Tests for REST API's read offer view for user with organization."""

    def setUp(self):
        """Set up each test."""
        super().setUp()
        self.organization = OrganizationFactory()
        self.client.force_login(UserFactory(
            userprofile__organizations=[self.organization]
        ))

    def test_published_offer_read_status(self):
        """Test published offer's read status for user with organization."""
        for offer in OfferFactory.create_batch(81, offer_status='published'):
            response = self.client.get('/api/offers/{id}/'.format(id=offer.id))
            self.assertEqual(response.status_code, status.HTTP_200_OK)
            common.test_offer_list_fields(self, response.data)

    def test_organization_offer_read_status(self):
        """Test organization offer's read status for user with organization."""
        for offer in OfferFactory.create_batch(
                94, organization=self.organization
        ):
            response = self.client.get('/api/offers/{id}/'.format(id=offer.id))
            self.assertEqual(response.status_code, status.HTTP_200_OK)
            common.test_offer_list_fields(self, response.data)

    def test_unpublished_offer_read_status(self):
        """Test unpublished offer's read status for user with organization."""
        for offer in OfferFactory.create_batch(12, offer_status='unpublished'):
            response = self.client.get('/api/offers/{id}/'.format(id=offer.id))
            self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_rejected_offer_read_status(self):
        """Test rejected offer's read status for user with organization."""
        for offer in OfferFactory.create_batch(12, offer_status='rejected'):
            response = self.client.get('/api/offers/{id}/'.format(id=offer.id))
            self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)


class TestRegularUserOffersReadAPIView(APITestCase):

    """Tests for REST API's read offer view for regular user."""

    def setUp(self):
        """Set up each test."""
        super().setUp()
        self.client.force_login(UserFactory())

    def test_published_offer_read_status(self):
        """Test published offer's read status for regular user."""
        for offer in OfferFactory.create_batch(28, offer_status='published'):
            response = self.client.get('/api/offers/{id}/'.format(id=offer.id))
            self.assertEqual(response.status_code, status.HTTP_200_OK)
            common.test_offer_list_fields(self, response.data)

    def test_unpublished_offer_read_status(self):
        """Test unpublished offer's read status for regular user."""
        for offer in OfferFactory.create_batch(33, offer_status='unpublished'):
            response = self.client.get('/api/offers/{id}/'.format(id=offer.id))
            self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_rejected_offer_read_status(self):
        """Test rejected offer's read status for regular user."""
        for offer in OfferFactory.create_batch(33, offer_status='rejected'):
            response = self.client.get('/api/offers/{id}/'.format(id=offer.id))
            self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)


class TestAnonymousUserOffersReadAPIView(APITestCase):

    """Tests for REST API's read offer view for anonymous user."""

    def test_published_offer_read_status(self):
        """Test published offer's read status for anonymous user."""
        for offer in OfferFactory.create_batch(41, offer_status='published'):
            response = self.client.get('/api/offers/{id}/'.format(id=offer.id))
            self.assertEqual(response.status_code, status.HTTP_200_OK)
            common.test_offer_list_fields(self, response.data)

    def test_unpublished_offer_read_status(self):
        """Test unpublished offer's read status for anonymous user."""
        for offer in OfferFactory.create_batch(57, offer_status='unpublished'):
            response = self.client.get('/api/offers/{id}/'.format(id=offer.id))
            self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_rejected_offer_read_status(self):
        """Test rejected offer's read status for anonymous user."""
        for offer in OfferFactory.create_batch(64, offer_status='rejected'):
            response = self.client.get('/api/offers/{id}/'.format(id=offer.id))
            self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
