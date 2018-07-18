# -*- coding: utf-8 -*-

"""
.. module:: factories
"""

import datetime
import os

from django.contrib.auth import get_user_model
from django.utils import timezone
import factory
from factory.django import ImageField
from factory.fuzzy import FuzzyChoice
import requests

from apps.volontulo.models import Offer
from apps.volontulo.models import Organization
from apps.volontulo.models import UserProfile


User = get_user_model()


class UserProfileFactory(factory.DjangoModelFactory):
    """Factory for user profile."""

    class Meta:  # pylint: disable=C0111
        model = UserProfile

    user = factory.SubFactory(
        "apps.volontulo.factories.UserFactory",
        userprofile=None
    )

    @factory.post_generation
    def organizations(self, create, extracted):
        """Manage m2m relation."""
        if not create:
            return
        if extracted:
            for org in extracted:
                self.organizations.add(org)

    phone_no = factory.Faker("phone_number", locale="pl_PL")


class UserFactory(factory.DjangoModelFactory):
    """Factory for User."""

    class Meta:  # pylint: disable=C0111
        model = User

    first_name = factory.Faker("first_name", locale="pl_PL")
    last_name = factory.Faker("last_name", locale="pl_PL")
    email = factory.Faker("email", locale="pl_PL")
    username = factory.LazyAttribute(lambda obj: obj.email)

    is_active = True
    password = "pass123"
    userprofile = factory.RelatedFactory(UserProfileFactory, "user")

    @classmethod
    def _create(cls, model_class, *args, **kwargs):
        manager = cls._get_manager(model_class)
        return manager.create_user(*args, **kwargs)


class OrganizationFactory(factory.DjangoModelFactory):
    """Factory for Organization."""

    def _organization_name():  # pylint: disable=E0211
        """Creates  a fake organization name.

        Fake name consist of predicate1 + subject + predicate2 + propername
        np. "Wojewódzka Alternatywa Organizacyjna "Naprzód"".
        """

        predicate1_dict = {
            "masculine": [
                "Krajowy", "Wojewódzki", "Powiatowy", "Regionalny",
                "Wielkopolski", "Osiedlowy", "Stołeczny"],
            "feminine": [
                "Krajowa", "Wojewódzka", "Powiatowa", "Regionalna",
                "Wielkopolska", "Osiedlowa", "Stołeczna"],
            "neutrum": [
                "Krajowe", "Wojewódzkie", "Powiatowe", "Regionalne",
                "Wielkopolskie", "Osiedlowe", "Stołeczne"]
        }
        noun_list = {
            "Fundacja": "feminine",
            "Rada": "feminine",
            "Urząd": "masculine",
            "Zarząd": "masculine",
            "Delegatura": "feminine",
            "Poradnia": "feminine",
            "Szpital": "masculine",
            "Ogród": "masculine",
            "Koło": "neutrum",
            "Obwód": "masculine"
        }
        predicate2_dict = {
            "masculine": [
                "Organizacyjny", "Rejestrowy", "Egzekutywny", "Wspierający",
                "Transakcyjny", "Związkowy", "Zbiorczy"],
            "feminine": [
                "Organizacyjna", "Rejestrowa", "Egzekutywna", "Wspierająca",
                "Transakcyjna", "Związkowa", "Zbiorcza"],
            "neutrum": [
                "Organizacyjne", "Rejestrowe", "Egzekutywne", "Wspierające",
                "Transakcyjne", "Związkowe", "Zbiorcze"]
        }

        propername_list = [
            "Wspiera się", "Totuus", "Zawsze Razem", "W Kupie Siła",
            "Al Capone", "UKF", "Smak Miesiąca"
        ]

        subject = (FuzzyChoice(noun_list.keys())).fuzz()
        predicate1 = (FuzzyChoice(predicate1_dict[noun_list[subject]])).fuzz()
        predicate2 = (FuzzyChoice(predicate2_dict[noun_list[subject]])).fuzz()
        propername = (FuzzyChoice(propername_list)).fuzz()

        return "{0} {1} {2} {3}".format(
            predicate1,
            subject,
            predicate2,
            propername
        )

    class Meta:  # pylint: disable=C0111
        model = Organization

    name = factory.fuzzy.FuzzyAttribute(_organization_name)
    address = factory.Faker("address", locale="pl_PL")
    description = factory.Faker("paragraph")


def placeimg_com_download(width, height, category):
    """"placeimg.com downloader generator.

    You can choose width, height and category and it will return argumentless
    callable that will donwload such images and return file-like object.
    """

    def wrapped_func():
        """Actual callable responsible for downloading images."""
        return requests.get('https://placeimg.com/{}/{}/{}'.format(
            width,
            height,
            category,
        ), stream=True).raw

    return wrapped_func


_now = timezone.now()
_offer_start_date_min = _now - datetime.timedelta(days=365)
_offer_start_date_max = _now + datetime.timedelta(days=364)


class OfferFactory(factory.DjangoModelFactory):
    """Factory for Offer"""

    class Meta:  # pylint: disable=C0111
        model = Offer

    organization = factory.SubFactory(OrganizationFactory)

    @factory.post_generation
    def volunteers(self, create, extracted):
        """Manage ManyToMany field"""

        if not create:
            # Simple build, do nothing.
            return

        if extracted:
            # A list of Users were passed in, use them
            for user in extracted:
                self.volunteers.add(user)

    @factory.lazy_attribute
    def finished_at(self):
        """Returns finished_at attribute based on started_at value.

        Value will be between started_at and one year in future.
        """
        return factory.fuzzy.FuzzyDateTime(
            self.started_at,
            _offer_start_date_max,
        ).fuzz() + datetime.timedelta(days=1)

    @factory.lazy_attribute
    def recruitment_end_date(self):
        """Returns recruitment_end_date attribute.

        Value will be between recruitment_start_date and one year in future.
        """
        return factory.fuzzy.FuzzyDateTime(
            self.recruitment_start_date,
            _offer_start_date_max,
        ).fuzz() + datetime.timedelta(days=1)

    @factory.lazy_attribute
    def reserve_recruitment_end_date(self):
        """Returns reserve_recruitment_end_date attribute.

        Value will be between reserve_recruitment_start_date and one year
        in future.
        """
        return factory.fuzzy.FuzzyDateTime(
            self.reserve_recruitment_start_date,
            _offer_start_date_max,
        ).fuzz() + datetime.timedelta(days=1)

    @factory.lazy_attribute
    def action_end_date(self):
        """Returns action_end_date attribute based on action_start_date value.

        Value will be between action_start_date and one year in future.
        """
        return factory.fuzzy.FuzzyDateTime(
            self.action_start_date,
            _offer_start_date_max,
        ).fuzz() + datetime.timedelta(days=1)

    description = factory.Faker("paragraph")
    requirements = factory.Faker("paragraph")
    time_commitment = factory.Faker("paragraph")
    benefits = factory.Faker("paragraph")
    location = factory.Faker("address", locale="pl_PL")
    title = factory.Faker("text", max_nb_chars=150)
    started_at = factory.fuzzy.FuzzyDateTime(
        _offer_start_date_min,
        _offer_start_date_max,
    )
    time_period = factory.Faker("text", max_nb_chars=150)
    offer_status = factory.fuzzy.FuzzyChoice(
        choices=("unpublished", "published", "rejected")
    )
    recruitment_status = factory.fuzzy.FuzzyChoice(
        choices=("open", "supplemental", "closed")
    )
    votes = factory.fuzzy.FuzzyChoice(choices=(True, False))
    recruitment_start_date = factory.fuzzy.FuzzyDateTime(
        _offer_start_date_min,
        _offer_start_date_max,
    )
    reserve_recruitment = factory.fuzzy.FuzzyChoice(choices=(True, False))
    reserve_recruitment_start_date = factory.fuzzy.FuzzyDateTime(
        _offer_start_date_min,
        _offer_start_date_max,
    )
    action_ongoing = factory.fuzzy.FuzzyChoice(choices=(True, False))
    constant_coop = factory.fuzzy.FuzzyChoice(choices=(True, False))
    action_start_date = factory.fuzzy.FuzzyDateTime(
        _offer_start_date_min,
        _offer_start_date_max,
    )
    volunteers_limit = factory.fuzzy.FuzzyInteger(0, 1000)
    reserve_volunteers_limit = factory.fuzzy.FuzzyInteger(0, 1000)
    weight = factory.fuzzy.FuzzyInteger(0, 1000)
    image = ImageField(from_path=os.path.join(
        os.path.dirname(__file__),
        'static/volontulo/img/volontulo_baner.png'
    ))
