# -*- coding: utf-8 -*-

"""
.. module:: common
"""

from apps.volontulo.factories import UserFactory
from apps.volontulo.factories import OfferFactory
from apps.volontulo.factories import OrganizationFactory


def initialize_empty_volunteer():
    """Initialize empty volunteer."""
    volunteer_user1 = UserFactory(
        email='volunteer1@example.com',
        password='volunteer1',
        first_name='Grzegorz',
        last_name='Brzęczyszczykiewicz',
        userprofile__phone_no='333666999',
    )
    return volunteer_user1


def initialize_empty_organization():
    """Initialize empty organization."""
    organization1 = OrganizationFactory()
    UserFactory(
        email='organization1@example.com',
        password='organization1',
        userprofile__organizations=[organization1]
    )
    return organization1


def initialize_filled_volunteer_and_organization():
    """Initialize volunteer filled with data."""

    # create volunteer user
    volunteer_user2 = UserFactory(
        email='volunteer2@example.com',
        password='volunteer2'
    )

    # create organization user to create offers
    organization2 = OrganizationFactory()
    # this is required due to login to this user
    UserFactory(
        email='organization2@example.com',
        password='organization2',
        userprofile__organizations=[organization2]
    )

    # create organization offers and assign volunteer to them
    for _ in range(11, 15):
        OfferFactory(
            organization=organization2,
            offer_status='published',
            volunteers=[volunteer_user2]
        )

    # create additional organization offers for administrator use
    for _ in range(100, 110):
        OfferFactory(
            organization=organization2,
            offer_status='unpublished',
        )

    return volunteer_user2, organization2


def test_offer_list_fields(self, offer):
    """Test read's fields of offers REST API endpoint."""
    self.assertIsInstance(offer.pop('action_status'), str)
    self.assertIsInstance(offer.pop('finished_at'), (str, type(None)))
    self.assertIsInstance(offer.pop('id'), int)
    self.assertIsInstance(offer.pop('image'), (str, type(None)))
    self.assertIsInstance(offer.pop('location'), str)
    self.assertIsInstance(offer.pop('offer_status'), str)
    self.assertIsInstance(offer.pop('slug'), str)
    self.assertIsInstance(offer.pop('started_at'), (str, type(None)))
    self.assertIsInstance(offer.pop('title'), str)
    self.assertIsInstance(offer.pop('url'), str)
    self.assertIsInstance(offer.pop('description'), str)
    self.assertIsInstance(offer.pop('benefits'), str)
    self.assertIsInstance(offer.pop('requirements'), str)
    self.assertIsInstance(offer.pop('time_commitment'), str)
    self.assertIsInstance(offer.pop('time_period'), str)
    self.assertIsInstance(offer.pop('recruitment_start_date'),
                          (str, type(None)))
    self.assertIsInstance(offer.pop('recruitment_end_date'), (str, type(None)))
    self.assertIsInstance(offer.pop('reserve_recruitment'), bool)
    self.assertIsInstance(offer.pop('reserve_recruitment_start_date'),
                          (str, type(None)))
    self.assertIsInstance(offer.pop('reserve_recruitment_end_date'),
                          (str, type(None)))
    self.assertIsInstance(offer.pop('action_ongoing'), bool)
    self.assertIsInstance(offer.pop('constant_coop'), bool)
    self.assertIsInstance(offer.pop('volunteers_limit'), int)
    self.assertIsInstance(offer.pop('reserve_volunteers_limit'), int)
    self.assertIsInstance(offer['organization'].pop('address'), str)
    self.assertIsInstance(offer['organization'].pop('description'), str)
    self.assertIsInstance(offer['organization'].pop('id'), int)
    self.assertIsInstance(offer['organization'].pop('name'), str)
    self.assertIsInstance(offer['organization'].pop('slug'), str)
    self.assertIsInstance(offer['organization'].pop('url'), str)
    self.assertEqual(len(offer.pop('organization')), 0)
    self.assertIsInstance(offer.pop('joined'), bool)
    self.assertEqual(len(offer), 0)
