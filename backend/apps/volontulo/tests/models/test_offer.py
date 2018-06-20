# -*- coding: utf-8 -*-

"""
.. module:: test_offer
"""

from django.test import TestCase

from apps.volontulo.factories import OfferFactory
from apps.volontulo.factories import UserFactory
from apps.volontulo.models import Offer
from apps.volontulo.models import Organization


class TestOfferModel(TestCase):
    """Tests for Offer model."""

    @classmethod
    def setUpTestData(cls):
        """Fixtures for Offer model unittests."""
        volunteers = [
            UserFactory(email='volunteer1@example.com'),
            UserFactory(email='volunteer2@example.com'),
            UserFactory(email='volunteer3@example.com'),
        ]
        offer = OfferFactory(
            organization__name='Some great organization',
            description='A lot of unnecessary work.',
            requirements='Patience, lot of free time',
            time_commitment='12.12.2015',
            benefits='Friends with benefits',
            location='Poland, Poznań',
            title='Example Offer Title',
            time_period='2-5 times a week',
        )
        for volunteer in volunteers:
            offer.volunteers.add(volunteer)

    def test__string_representation(self):
        """Test Offer model string reprezentation."""
        offer = Offer.objects.get(title='Example Offer Title')

        self.assertEqual(offer.volunteers.count(), 3)
        self.assertEqual(
            offer.volunteers.all()[0].email,
            'volunteer1@example.com'
        )
        self.assertEqual(
            offer.volunteers.all()[1].email,
            'volunteer2@example.com'
        )
        self.assertEqual(
            offer.volunteers.all()[2].email,
            'volunteer3@example.com'
        )
        self.assertEqual(offer.organization.name, 'Some great organization')
        self.assertEqual(offer.description, 'A lot of unnecessary work.')
        self.assertEqual(offer.requirements, 'Patience, lot of free time')
        self.assertEqual(offer.time_commitment, '12.12.2015')
        self.assertEqual(offer.benefits, 'Friends with benefits')
        self.assertEqual(offer.location, 'Poland, Poznań')
        self.assertEqual(offer.time_period, '2-5 times a week')


class OfferTestCase(TestCase):
    """Tests for Offer model."""

    def setUp(self):
        self.offer = OfferFactory(
            organization__name="Halperin Organix",
            description="Dokładny opis oferty",
            requirements="Dokładny opis wymagań",
            time_commitment="333 dni w roku",
            benefits="Wszelkie korzyści z uczestnictwa w wolontariacie",
            location="Polska, Poznań",
            title="Zwięzły tytuł oferty",
            time_period="Od 23.09.2015 do 25.12.2016",
        )

    def test__offer_organization_field(self):
        """Testing organization name as oneToOne relation"""
        self.assertIsInstance(self.offer.organization, Organization)
        self.assertEqual(self.offer.organization.name, "Halperin Organix")

    def test__offer_description_field(self):
        """Testing offer description field"""
        self.assertEqual(self.offer.description, "Dokładny opis oferty")

    def test__offer_requiremends_field(self):
        """Testing offer requirements field"""
        self.assertEqual(self.offer.requirements, "Dokładny opis wymagań")

    def test__offer_time_commit_field(self):
        """Testing offer time commitment field"""
        self.assertEqual(self.offer.time_commitment, "333 dni w roku")

    def test__offer_benefits_field(self):
        """Testing offer benefits field"""
        self.assertEqual(
            self.offer.benefits,
            "Wszelkie korzyści z uczestnictwa w wolontariacie"
        )

    def test__offer_location_field(self):
        """Testing offer location field"""
        self.assertEqual(self.offer.location, "Polska, Poznań")

    def test__offer_title_field(self):
        """Testing offer title field"""
        self.assertEqual(self.offer.title, "Zwięzły tytuł oferty")

    def test__offer_time_period_field(self):
        """Testing offer time_period field"""
        self.assertEqual(self.offer.time_period, "Od 23.09.2015 do 25.12.2016")
