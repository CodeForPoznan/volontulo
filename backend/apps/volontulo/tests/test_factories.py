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
from apps.volontulo.models import Organization, Offer


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

    """Test for OfferFactory."""

    def setUp(self):
        """Set up test for OfferFactory"""

        self.fake_user1 = UserFactory.create(
            first_name="Fake user first_name1",
            last_name="Fake user last_name1"
        )
        self.fake_user2 = UserFactory.create(
            first_name="Fake user first_name2",
            last_name="Fake user last_name2"
        )
        self.fake_offer1 = OfferFactory.create(volunteers=User.objects.all())
        self.fake_offer2 = OfferFactory.create(
            title="Jakiś tytuł",
            description="Zwięzły opis",
            organization__name="Nazwa odnośnej organizacji"
        )
        self.fake_offer3 = OfferFactory.create(
            organization=Organization.objects.last()
        )

    def test_if_users_have_been_created(self):
        """Test if fake users have been created."""
        self.assertEqual(User.objects.count(), 2)

    def test_if_fake_organization_has_been_created(self):
        """Test fake organization created by SubFactory."""
        self.assertEqual(Organization.objects.count(), 2)

    def test_if_offer_has_been_created(self):
        """Test if offer has been created."""
        created_offer = Offer.objects.get(title="Jakiś tytuł")
        self.assertEqual(created_offer.description, "Zwięzły opis")

    def test_if_offer_is_connected_with_some_organization(self):
        """Test if offer is connected with organization."""
        fake_offer_with_organization = Offer.objects.filter(
            title="Jakiś tytuł"
        )[0]
        self.assertTrue(
            fake_offer_with_organization.organization.name,
            "Nazwa odnośnej organizacji"
        )

    def test_if_offer_is_connected_with_some_volonteer(self):
        """Test if offer is connected with volunteer."""
        fake_offer = Offer.objects.all()[0]
        fake_offer_volunteers1 = fake_offer.volunteers.filter(
            first_name="Fake user first_name1"
        )
        connected_user1 = fake_offer_volunteers1[0]
        fake_offer_volunteers2 = fake_offer.volunteers.filter(
            first_name="Fake user first_name2"
        )
        connected_user2 = fake_offer_volunteers2[0]
        self.assertTrue(connected_user1.last_name, "Fake user last_name1")
        self.assertTrue(connected_user2.last_name, "Fake user last_name2")

    def test_offers_paragraph_is_str(self):
        """Test if offers textFields are str and chr>0."""
        description = self.fake_offer1.description
        self.assertIsInstance(description, str)
        self.assertTrue(len(description) > 0)
        requirements = self.fake_offer1.requirements
        self.assertIsInstance(requirements, str)
        self.assertTrue(len(requirements) > 0)
        time_commitment = self.fake_offer1.time_commitment
        self.assertIsInstance(time_commitment, str)
        self.assertTrue(len(time_commitment) > 0)
        time_commitment = self.fake_offer1.time_commitment
        self.assertIsInstance(time_commitment, str)
        self.assertTrue(len(time_commitment) > 0)
        title = self.fake_offer1.title
        self.assertIsInstance(title, str)
        self.assertTrue(len(title) > 0)
        time_period = self.fake_offer1.time_period
        self.assertIsInstance(time_period, str)
        self.assertTrue(len(time_period) > 0)
        location = self.fake_offer1.location
        self.assertIsInstance(location, str)
        self.assertTrue(len(location) > 0)

    def test_offers_boolean_fields(self):
        """Test if offers booleanFields are 0 or 1."""
        self.assertIsInstance(self.fake_offer1.votes, bool)
        self.assertIsInstance(self.fake_offer1.reserve_recruitment, bool)
        self.assertIsInstance(self.fake_offer1.action_ongoing, bool)
        self.assertIsInstance(self.fake_offer1.constant_coop, bool)

    def test_offers_datatime_fields(self):
        """Test if offers datatimeFields are proper type."""
        self.assertIsInstance(self.fake_offer1.started_at, datetime.datetime)
        self.assertIsInstance(self.fake_offer1.started_at, datetime.datetime)
        self.assertIsInstance(
            self.fake_offer1.recruitment_start_date,
            datetime.datetime
        )
        self.assertIsInstance(
            self.fake_offer1.reserve_recruitment_start_date,
            datetime.datetime
        )
        self.assertIsInstance(
            self.fake_offer1.reserve_recruitment_end_date,
            datetime.datetime
        )
        self.assertIsInstance(
            self.fake_offer1.action_start_date,
            datetime.datetime
        )
        self.assertIsInstance(
            self.fake_offer1.action_end_date,
            datetime.datetime
        )

    def test_offer_if_choices_takes_proper_values(self):
        """Test if fields with choices takes proper values."""
        self.assertIn(
            self.fake_offer1.offer_status,
            ["unpublished", "published", "rejected"]
        )
        self.assertIn(
            self.fake_offer1.recruitment_status,
            ["open", "supplemental", "closed"]
        )
        self.assertIn(
            self.fake_offer1.action_status,
            ["future", "ongoing", "finished"]
        )

    def test_offer_if_integerField_are_proper_type(self):
        """Test if integerField is int type."""
        self.assertIsInstance(self.fake_offer1.volunteers_limit, int)
        self.assertIsInstance(self.fake_offer1.reserve_volunteers_limit, int)
        self.assertIsInstance(self.fake_offer1.weight, int)


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
