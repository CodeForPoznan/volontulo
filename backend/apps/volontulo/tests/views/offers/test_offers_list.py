"""
.. module:: test_offers_list
"""

from django.test import Client
from django.test import TestCase

from apps.volontulo.factories import OfferFactory
from apps.volontulo.factories import OrganizationFactory
from apps.volontulo.factories import UserFactory


class TestOffersList(TestCase):
    """Class responsible for testing offers' list."""

    def setUp(self):
        """Set up each test."""
        self.client = Client()

    def _test_offers_list(self, response):
        """Test offers' list."""
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'offers/offers_list.html')
        self.assertIn('offers', response.context)

    def test_offer_list_for_anonymous_user(self):
        """Test offers' list for anonymus user."""
        OfferFactory.create_batch(
            31,
            offer_status='published',
            finished_at=None,
            recruitment_end_date=None,
        )
        OfferFactory.create_batch(48, offer_status='unpublished')
        OfferFactory.create_batch(52, offer_status='rejected')

        response = self.client.get('/o/offers')

        self._test_offers_list(response)
        self.assertEqual(len(response.context['offers']), 31)

    def test_offers_list_for_volunteer(self):
        """Test offers' list for account of volunteer."""
        OfferFactory.create_batch(
            67,
            offer_status='published',
            finished_at=None,
            recruitment_end_date=None,
        )
        OfferFactory.create_batch(73, offer_status='unpublished')
        OfferFactory.create_batch(89, offer_status='rejected')

        self.client.force_login(UserFactory())

        response = self.client.get('/o/offers')

        self._test_offers_list(response)
        self.assertEqual(len(response.context['offers']), 67)

    def test_offers_list_for_organization(self):
        """Test offers' list for account of organization."""
        OfferFactory.create_batch(
            96,
            offer_status='published',
            finished_at=None,
            recruitment_end_date=None,
        )
        OfferFactory.create_batch(17, offer_status='unpublished')
        OfferFactory.create_batch(22, offer_status='rejected')

        self.client.force_login(UserFactory(
            userprofile__organizations=[OrganizationFactory()]
        ))

        response = self.client.get('/o/offers')

        self._test_offers_list(response)
        self.assertEqual(len(response.context['offers']), 96)

    def test_offers_list_for_admin(self):
        """Test offers' list for account of admin."""
        OfferFactory.create_batch(37)

        self.client.force_login(UserFactory(
            userprofile__is_administrator=True
        ))

        response = self.client.get('/o/offers')

        self._test_offers_list(response)
        self.assertEqual(len(response.context['offers']), 37)
