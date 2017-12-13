# -*- coding: utf-8 -*-

"""
.. module:: common
"""

from django.contrib.auth.models import User

from apps.volontulo.models import Offer
from apps.volontulo.models import Organization
from apps.volontulo.models import UserProfile

COMMON_OFFER_DATA = {
    'organization': None,
    'description': '',
    'requirements': '',
    'time_commitment': '',
    'benefits': '',
    'location': '',
    'title': 'volontulo offer',
    'time_period': ''
}


def initialize_empty_volunteer():
    """Initialize empty volunteer."""
    volunteer_user1 = User.objects.create_user(
        'volunteer1@example.com',
        'volunteer1@example.com',
        'volunteer1',
        first_name='Grzegorz',
        last_name='Brzęczyszczykiewicz',
    )
    volunteer_user1.save()
    userprofile = UserProfile.objects.create(user=volunteer_user1)
    userprofile.phone_no = '333666999'
    userprofile.save()
    return volunteer_user1


def initialize_empty_organization():
    """Initialize empty organization."""
    organization1 = Organization.objects.create(
        name='Organization 1',
        address='Organization 1 address',
        description='Organization 1 description',
    )
    organization1.save()
    organization_user1 = User.objects.create_user(
        'organization1@example.com',
        'organization1@example.com',
        'organization1',
        first_name='Organization1Firstname',
        last_name='Organization1Lastname',
    )
    organization_user1.save()
    organization_profile1 = UserProfile.objects.create(
        user=organization_user1,
    )
    organization_profile1.organizations.add(organization1)
    return organization1


def initialize_filled_volunteer_and_organization():
    """Initialize volunteer filled with data."""
    # create volunteer user
    volunteer_user2 = User.objects.create_user(
        'volunteer2@example.com',
        'volunteer2@example.com',
        'volunteer2'
    )
    volunteer_user2.save()
    UserProfile.objects.create(user=volunteer_user2)

    # create organization user to create offers
    organization2 = Organization.objects.create(name='Organization 2')
    organization2.save()
    # this is required due to login to this user
    organization_user2 = User.objects.create_user(
        'organization2@example.com',
        'organization2@example.com',
        'organization2'
    )
    organization_user2.save()
    organization_profile2 = UserProfile.objects.create(
        user=organization_user2,
    )
    organization_profile2.organizations.add(organization2)

    # create organization offers and assign volunteer to them
    for i in range(11, 15):
        offer = Offer.objects.create(
            title='Title {}'.format(i),
            description='Description {}'.format(i),
            requirements='Requirements {}'.format(i),
            time_commitment='Time commitment {}'.format(i),
            benefits='Benefits {}'.format(i),
            location='Location {}'.format(i),
            time_period='Time period {}'.format(i),
            status_old='ACTIVE',
            votes=True,
            started_at='2015-10-05 09:10:11+00:00',
            finished_at='2015-12-12 12:13:14+00:00',
            organization=organization2,
            offer_status='published',
            recruitment_status='open',
            action_status='ongoing',
        )
        offer.volunteers.add(volunteer_user2)
        offer.save()

    # create additional organization offers for administrator use
    for i in range(100, 110):
        offer2 = Offer.objects.create(
            title='Title {}'.format(i),
            description='Description {}'.format(i),
            requirements='Requirements {}'.format(i),
            time_commitment='Time commitment {}'.format(i),
            benefits='Benefits {}'.format(i),
            location='Location {}'.format(i),
            time_period='Time period {}'.format(i),
            status_old='SUSPENDED' if i % 2 == 0 else 'NEW',
            votes=True,
            started_at='2015-10-05 09:10:11+00:00',
            finished_at='2015-12-12 12:13:14+00:00',
            organization=organization2,
            offer_status='unpublished',
            recruitment_status='open',
            action_status='ongoing',
        )
        offer2.save()

    return volunteer_user2, organization2


def initialize_empty_organizations():
    """Initialize empty organization."""
    for i in range(11, 15):
        organization = Organization.objects.create(
            id=i,
            name='Organization {}'.format(i)
        )
        organization.save()
        organization_user = User.objects.create_user(
            'organization{}@example.com'.format(i),
            'organization{}@example.com'.format(i),
            'organization{}'.format(i)
        )
        organization_user.save()
        user_profile = UserProfile.objects.create(
            user=organization_user,
        )
        user_profile.organizations.add(organization)


def initialize_administrator(
        username='admin_user@example.com',
        email='admin_user@example.com', password='admin_password'):
    """Initialize administrator user.

    :param username: string User username
    :param email: string User email
    :param password: string User plaintext password
    """
    administrator1 = User.objects.create_user(username, email, password)
    administrator1.save()
    administrator_profile = UserProfile.objects.create(user=administrator1)
    administrator_profile.is_administrator = True
    administrator_profile.save()
    return administrator1


def test_offer_list_fields(self, offer):
    """Test read's fields of offers REST API endpoint."""
    self.assertIsInstance(offer.pop('finished_at'), str)
    self.assertIsInstance(offer.pop('id'), int)
    self.assertIsInstance(offer.pop('image'), (str, type(None)))
    self.assertIsInstance(offer.pop('location'), str)
    self.assertIsInstance(offer.pop('slug'), str)
    self.assertIsInstance(offer.pop('started_at'), str)
    self.assertIsInstance(offer.pop('title'), str)
    self.assertIsInstance(offer.pop('url'), str)
    self.assertIsInstance(offer.pop('description'), str)
    self.assertIsInstance(offer.pop('benefits'), str)
    self.assertIsInstance(offer.pop('requirements'), str)
    self.assertIsInstance(offer.pop('time_commitment'), str)
    self.assertIsInstance(offer.pop('time_period'), str)
    self.assertIsInstance(offer.pop('recruitment_end_date'), (str, type(None)))
    self.assertIsInstance(offer['organization'].pop('address'), str)
    self.assertIsInstance(offer['organization'].pop('description'), str)
    self.assertIsInstance(offer['organization'].pop('id'), int)
    self.assertIsInstance(offer['organization'].pop('name'), str)
    self.assertIsInstance(offer['organization'].pop('slug'), str)
    self.assertIsInstance(offer['organization'].pop('url'), str)
    self.assertEqual(len(offer.pop('organization')), 0)
    self.assertEqual(len(offer), 0)
