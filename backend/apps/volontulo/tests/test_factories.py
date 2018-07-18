# -*- coding: utf-8 -*-

"""
.. module:: test_factories
"""

import datetime
from unittest import mock

from django.contrib.auth.models import User
from django.test import TestCase

from apps.volontulo.factories import OfferFactory
from apps.volontulo.factories import OrganizationFactory
from apps.volontulo.factories import placeimg_com_download
from apps.volontulo.factories import UserFactory
from apps.volontulo.factories import UserProfileFactory
from apps.volontulo.models import Offer
from apps.volontulo.models import Organization


class UserFactoryTestCase(TestCase):

    """Test for UserFactory."""

    def setUp(self):
        """setting up each test."""
        UserFactory.create(first_name="nie-Jan", last_name="nie-Kowalski")
        self.totally_fake_user = UserFactory.create()

    def test_factories_write_to_db(self):
        """Test if UserFactory properly create fake user."""
        self.assertEqual(User.objects.count(), 2)

    def test_UserFactory_firstname_lastname(self):
        """Test if UserFactory first_name fits to last_name."""
        tested_user = User.objects.get(first_name="nie-Jan")
        self.assertEqual(tested_user.last_name, "nie-Kowalski")

    def test_UserFactory_faker_if_first_last_name_is_str(self):
        """Test if created user.first_name,last_name is str and char>0."""
        self.assertTrue(isinstance(self.totally_fake_user.first_name, str))
        self.assertTrue(isinstance(self.totally_fake_user.last_name, str))
        self.assertTrue(len(self.totally_fake_user.first_name) > 0)
        self.assertTrue(len(self.totally_fake_user.last_name) > 0)

    def test_userfactory_faker_if_email_has_at(self):
        """Test if email of last created user contains an @. """
        self.assertIn("@", self.totally_fake_user.email)

    def test_userfactory_faker_email_is_the_same_as_username(self):
        """Test if email equals user_name."""
        self.assertEqual(
            self.totally_fake_user.email,
            self.totally_fake_user.username
        )


class UserProfileFactoryTestCase(TestCase):

    """Test for UserProfileFactory."""

    def setUp(self):
        OrganizationFactory.create(
            name="Nazwa organizacji1",
        )
        OrganizationFactory.create()
        # User is created as a Subfactory of UserProfile
        self.fake_user_profile = UserProfileFactory.create(
            user__first_name="Edmund",
            organizations=Organization.objects.all(),
            phone_no="22909"
        )

    def test_if_user_profile_has_been_created(self):
        """Test if UserProfile has been created."""
        self.assertEqual(self.fake_user_profile.phone_no, "22909")

    def test_if_user_profile_is_connected_to_user(self):
        """Test if UserProfile is connected to User."""
        self.assertEqual(self.fake_user_profile.user.first_name, "Edmund")

    def test_if_organizations_can_be_connected_with_User_Profile(self):
        """Test m2m relation UserProfile-Organizations."""
        organizations = self.fake_user_profile.organizations.all()
        self.assertEqual(len(organizations), 2)
        self.assertEqual(organizations[0].name, "Nazwa organizacji1")

    def test_UserProfile_is_administrator_field(self):
        """Test UserProfile is_administrator field."""
        self.assertIsInstance(self.fake_user_profile.is_administrator, bool)

    def test_UserProfil_phone_no_field(self):
        """Test UserProfile phone_no field."""
        self.assertFalse(self.fake_user_profile.phone_no.isalpha())


class OrganizationFactoryTestCase(TestCase):

    """Test for OrganizationFactory."""

    def setUp(self):
        """Set up each test"""
        OrganizationFactory.create(
            name="Flota zjednoczonych sił",
            address="Psia Wólka"
        )
        self.fake_organization = OrganizationFactory.create()

    def test_organizationfactory(self):
        """Test if OrganizationFactory.create creates new Organization."""
        test_organization = Organization.objects.get(
            name="Flota zjednoczonych sił"
        )
        self.assertEqual(test_organization.address, "Psia Wólka")

    def test_organization_if_name_address_description_is_str(self):
        """Test if organization name/address/description is str and char>0."""
        self.assertTrue(isinstance(self.fake_organization.name, str))
        self.assertTrue(isinstance(self.fake_organization.address, str))
        self.assertTrue(isinstance(self.fake_organization.description, str))
        self.assertTrue(len(self.fake_organization.name) > 0)
        self.assertTrue(len(self.fake_organization.address) > 0)
        self.assertTrue(len(self.fake_organization.description) > 0)


class OfferFactoryTestCase(TestCase):

    """Tests for OfferFactory."""

    def setUp(self):
        self.offer = OfferFactory(volunteers=UserFactory.create_batch(10))

    def test_if_organization_has_been_created(self):
        """Test if organization was created by SubFactory."""
        self.assertEqual(Organization.objects.count(), 1)

    def test_if_offer_has_been_created(self):
        """Test if offer was created."""
        self.assertEqual(Offer.objects.count(), 1)

    def test_if_offer_is_connected_with_some_organization(self):
        """Test if offer is connected with organization."""
        self.assertEqual(self.offer.organization, Organization.objects.get())

    def test_if_volunteers_were_added_to_offer(self):
        """Test if offer contains created volunteers."""
        self.assertEqual(self.offer.volunteers.count(), 10)

    def test_offers_string_fields(self):
        """Test if offers text fields are strings and not empty."""
        self.assertIsInstance(self.offer.description, str)
        self.assertGreater(len(self.offer.description), 0)

        self.assertIsInstance(self.offer.requirements, str)
        self.assertGreater(len(self.offer.requirements), 0)

        self.assertIsInstance(self.offer.time_commitment, str)
        self.assertGreater(len(self.offer.time_commitment), 0)

        self.assertIsInstance(self.offer.title, str)
        self.assertGreater(len(self.offer.title), 0)

        self.assertIsInstance(self.offer.time_period, str)
        self.assertGreater(len(self.offer.time_period), 0)

        self.assertIsInstance(self.offer.location, str)
        self.assertGreater(len(self.offer.location), 0)

    def test_offers_boolean_fields(self):
        """Test if offers boolean fields contain boolean value."""
        self.assertIsInstance(self.offer.votes, bool)
        self.assertIsInstance(self.offer.reserve_recruitment, bool)
        self.assertIsInstance(self.offer.action_ongoing, bool)
        self.assertIsInstance(self.offer.constant_coop, bool)

    def test_offers_datatime_fields(self):
        """Test if offers date fields are proper type and in proper order."""
        self.assertIsInstance(self.offer.started_at, datetime.datetime)
        self.assertIsInstance(self.offer.started_at, datetime.datetime)
        self.assertGreater(self.offer.finished_at, self.offer.started_at)

        self.assertIsInstance(
            self.offer.recruitment_start_date,
            datetime.datetime
        )
        self.assertIsInstance(
            self.offer.recruitment_end_date,
            datetime.datetime
        )
        self.assertGreater(
            self.offer.recruitment_end_date,
            self.offer.recruitment_start_date,
        )

        self.assertIsInstance(
            self.offer.reserve_recruitment_start_date,
            datetime.datetime
        )
        self.assertIsInstance(
            self.offer.reserve_recruitment_end_date,
            datetime.datetime
        )
        self.assertGreater(
            self.offer.reserve_recruitment_end_date,
            self.offer.reserve_recruitment_start_date,
        )

        self.assertIsInstance(
            self.offer.action_start_date,
            datetime.datetime
        )
        self.assertIsInstance(
            self.offer.action_end_date,
            datetime.datetime
        )
        self.assertGreater(
            self.offer.action_end_date,
            self.offer.action_start_date,
        )

    def test_offer_if_choices_takes_proper_values(self):
        """Test if fields with choices takes proper values."""
        self.assertIn(
            self.offer.offer_status,
            ("unpublished", "published", "rejected")
        )
        self.assertIn(
            self.offer.recruitment_status,
            ("open", "supplemental", "closed")
        )

    def test_offer_integer_fields(self):
        """Test if integer fields contain integer value."""
        self.assertIsInstance(self.offer.volunteers_limit, int)
        self.assertIsInstance(self.offer.reserve_volunteers_limit, int)
        self.assertIsInstance(self.offer.weight, int)


class PlaceimComDownloadTestCase(TestCase):

    """Test factories helper responsible for downloading random images."""

    @staticmethod
    @mock.patch('requests.get')
    def test_external_url_request(get_mock):
        """Test if proper url is requested."""
        image_from_function = placeimg_com_download(1000, 400, 'any')

        image_from_function()

        get_mock.assert_called_with(
            'https://placeimg.com/1000/400/any',
            stream=True
        )
