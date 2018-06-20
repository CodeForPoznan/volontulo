# -*- coding: utf-8 -*-

"""
.. module:: test_offerstatus
"""

from datetime import timedelta

from django.test import TestCase
from django.utils import timezone

from apps.volontulo.factories import OfferFactory
from apps.volontulo.models import Offer


class TestOfferStatusModel(TestCase):
    """Tests for OfferStatus model."""

    @classmethod
    def setUpTestData(cls):
        """Fixtures for OfferStatus model unittests."""
        current_datetime = timezone.now()
        past = current_datetime - timedelta(days=5)
        future = current_datetime + timedelta(days=5)

        # closed offer (both dates in past)
        OfferFactory(
            started_at=str(past - timedelta(days=2)),
            finished_at=str(past),
            title='Offer 1',
        )

        # future offer (both dates in future)
        OfferFactory(
            started_at=str(future),
            finished_at=str(future + timedelta(days=2)),
            title='Offer 2',
        )

        # ongoing offer (start + end date)
        OfferFactory(
            started_at=str(past),
            finished_at=str(future),
            title='Offer 3',
        )

        # ongoing offer (start date, no ending before now)
        OfferFactory(
            started_at=str(past),
            finished_at=None,
            title='Offer 4',
        )

        # ongoing offer (end date, no start date)
        OfferFactory(
            started_at=None,
            finished_at=str(future),
            title='Offer 5',
        )

        # ongoing offer (no dates)
        OfferFactory(
            started_at=None,
            finished_at=None,
            title='Offer 6',
        )

        # closed offer (no start date, past end date)
        OfferFactory(
            started_at=None,
            finished_at=str(past),
            title='Offer 7',
        )

        # future offer (start date in future, no end date)
        OfferFactory(
            started_at=str(future),
            finished_at=None,
            title='Offer 8',
        )

    def test__determine_action_status(self):
        """Verify action status."""
        finished_offer = Offer.objects.get(title='Offer 1')
        self.assertEqual(finished_offer.action_status, 'finished')

        future_offer = Offer.objects.get(title='Offer 2')
        self.assertEqual(future_offer.action_status, 'future')

        ongoing_offer1 = Offer.objects.get(title='Offer 3')
        self.assertEqual(ongoing_offer1.action_status, 'ongoing')

        ongoing_offer2 = Offer.objects.get(title='Offer 4')
        self.assertEqual(ongoing_offer2.action_status, 'ongoing')

        ongoing_offer3 = Offer.objects.get(title='Offer 5')
        self.assertEqual(ongoing_offer3.action_status, 'ongoing')

        ongoing_offer4 = Offer.objects.get(title='Offer 6')
        self.assertEqual(ongoing_offer4.action_status, 'ongoing')

        finished_offer2 = Offer.objects.get(title='Offer 7')
        self.assertEqual(finished_offer2.action_status, 'finished')

        future_offer2 = Offer.objects.get(title='Offer 8')
        self.assertEqual(future_offer2.action_status, 'future')
