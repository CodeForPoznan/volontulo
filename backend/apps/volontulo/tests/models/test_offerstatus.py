# -*- coding: utf-8 -*-

"""
.. module:: test_offerstatus
"""

from datetime import timedelta

from django.test import TestCase
from django.utils import timezone

from apps.volontulo.models import Offer
from apps.volontulo.models import Organization


class TestOfferStatusModel(TestCase):
    """Tests for OfferStatus model."""

    @classmethod
    def setUpTestData(cls):
        """Fixtures for OfferStatus model unittests."""
        current_datetime = timezone.now()
        past = current_datetime - timedelta(days=5)
        future = current_datetime + timedelta(days=5)

        # closed offer
        Offer.objects.create(
            organization=Organization.objects.create(
                name='Some organization',
                address='',
                description=''
            ),
            started_at=str(past - timedelta(days=2)),
            finished_at=str(past),
            description='',
            requirements='',
            time_commitment='12.12.2015',
            benefits='',
            location='',
            title='Offer 1',
            time_period='',
        )

        # future offer
        Offer.objects.create(
            organization=Organization.objects.create(
                name='Some organization',
                address='',
                description=''
            ),
            started_at=str(future),
            finished_at=str(future + timedelta(days=2)),
            description='',
            requirements='',
            time_commitment='12.12.2015',
            benefits='',
            location='',
            title='Offer 2',
            time_period='',
        )

        # ongoing offer (start + end date)
        Offer.objects.create(
            organization=Organization.objects.create(
                name='Some organization',
                address='',
                description=''
            ),
            started_at=str(past),
            finished_at=str(future),
            description='',
            requirements='',
            time_commitment='12.12.2015',
            benefits='',
            location='',
            title='Offer 3',
            time_period='',
        )

        # ongoing offer (start date, no ending before now)
        Offer.objects.create(
            organization=Organization.objects.create(
                name='Some organization',
                address='',
                description=''
            ),
            started_at=str(past),
            finished_at=None,
            description='',
            requirements='',
            time_commitment='12.12.2015',
            benefits='',
            location='',
            title='Offer 4',
            time_period='',
        )

    def test__determine_action_status(self):
        """Verify action status."""
        finished_offer = Offer.objects.get(title='Offer 1')
        self.assertEqual(finished_offer.determine_action_status(), 'finished')

        future_offer = Offer.objects.get(title='Offer 2')
        self.assertEqual(future_offer.determine_action_status(), 'future')

        ongoing_offer1 = Offer.objects.get(title='Offer 3')
        self.assertEqual(ongoing_offer1.determine_action_status(), 'ongoing')

        ongoing_offer2 = Offer.objects.get(title='Offer 4')
        self.assertEqual(ongoing_offer2.determine_action_status(), 'ongoing')
