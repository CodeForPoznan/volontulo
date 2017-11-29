"""
.. module:: test_factories
"""

from django.contrib.auth.models import User
from django.test import TestCase

from apps.volontulo.factories import UserFactory, OrganizationFactory
from apps.volontulo.models import Organization


class UserFactoryTestCase(TestCase):
    """Test for UserFactory."""
    def setUp(self):
        """setting up each test."""
        UserFactory.create(first_name='nie-Jan', last_name='nie-Kowalski')
        self.totally_fake_user = UserFactory.create()
        print(self.totally_fake_user)

    def test_factories_write_to_db(self):
        """Test if UserFactory properly create fake user."""
        self.assertEqual(User.objects.count(), 2)

    def test_UserFactory_firstname_lastname(self):
        """test if UserFactory first_name fits to last_name."""
        tested_user = User.objects.get(first_name='nie-Jan')
        self.assertEqual(tested_user.last_name, 'nie-Kowalski')

    def test_UserFactory_faker_if_first_last_name_is_str(self):
        """test if created user.first_name,last_name is str and char>0."""
        self.assertTrue(isinstance(self.totally_fake_user.first_name, str))
        self.assertTrue(isinstance(self.totally_fake_user.last_name, str))
        self.assertTrue(len(self.totally_fake_user.first_name) > 0)
        self.assertTrue(len(self.totally_fake_user.last_name) > 0)

    def test_userfactory_faker_if_email_has_at(self):
        """test wether email of last created user contains an @. """
        self.assertIn('@', self.totally_fake_user.email)

    def test_userfactory_faker_email_is_the_same_as_username(self):
        """test if email equals user_name."""
        self.assertEqual(
            self.totally_fake_user.email,
            self.totally_fake_user.username
            )


class OrganizationFactoryTestCase(TestCase):
    """Test for OrganizationFactory."""
    def setUp(self):
        """Set up each test"""
        OrganizationFactory.create(
            name='Flota zjednoczonych sił',
            address='Psia Wólka'
            )
        self.fake_organization = OrganizationFactory.create()

    def test_organizationfactory(self):
        """test if OrganizationFactory.create creates new Organization."""
        test_organization = Organization.objects.get(
            name='Flota zjednoczonych sił'
        )
        self.assertEqual(test_organization.address, 'Psia Wólka')

    def test_organization_if_name_address_description_is_str(self):
        """test if organization name/address/description is str and char>0."""
        self.assertTrue(isinstance(self.fake_organization.name, str))
        self.assertTrue(isinstance(self.fake_organization.address, str))
        self.assertTrue(isinstance(self.fake_organization.description, str))
        self.assertTrue(len(self.fake_organization.name) > 0)
        self.assertTrue(len(self.fake_organization.address) > 0)
        self.assertTrue(len(self.fake_organization.description) > 0)
