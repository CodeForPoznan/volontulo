# -*- coding: utf-8 -*-

"""
.. module:: factories
"""

from django.contrib.auth import get_user_model
import factory
from factory.fuzzy import FuzzyChoice

from apps.volontulo.models import Organization, UserProfile


User = get_user_model()


class UserProfileFactory(factory.DjangoModelFactory):
    """Factory for user profile."""

    class Meta:  # pylint: disable=C0111
        model = UserProfile


class UserFactory(factory.DjangoModelFactory):
    """Factory for User."""

    class Meta:  # pylint: disable=C0111
        model = User

    first_name = factory.Faker('first_name', locale='pl_PL')
    last_name = factory.Faker('last_name', locale='pl_PL')
    email = factory.Faker('email', locale='pl_PL')
    username = factory.LazyAttribute(lambda obj: obj.email)

    is_active = True
    password = 'password123'
    userprofile = factory.RelatedFactory(UserProfileFactory, 'user')

    @classmethod
    def _create(cls, model_class, *args, **kwargs):
        manager = cls._get_manager(model_class)
        return manager.create_user(*args, **kwargs)


class OrganizationFactory(factory.DjangoModelFactory):
    """Factory for Organization."""

    def _organization_name():  # pylint: disable=E0211
        """Creates  a fake organization name.

        Fake name consist of predicate1 + subject + predicate2 + propername
        np. 'Wojewódzka Alternatywa Organizacyjna "Naprzód"'.
        """

        predicate1_dict = {
            'masculine': [
                'Krajowy', 'Wojewódzki', 'Powiatowy', 'Regionalny',
                'Wielkopolski', 'Osiedlowy', 'Stołeczny'],
            'feminine': [
                'Krajowa', 'Wojewódzka', 'Powiatowa', 'Regionalna',
                'Wielkopolska', 'Osiedlowa', 'Stołeczna'],
            'neutrum': [
                'Krajowe', 'Wojewódzkie', 'Powiatowe', 'Regionalne',
                'Wielkopolskie', 'Osiedlowe', 'Stołeczne']
            }
        noun_list = {
            'Fundacja': 'feminine',
            'Rada': 'feminine',
            'Urząd': 'masculine',
            'Zarząd': 'masculine',
            'Delegatura': 'feminine',
            'Poradnia': 'feminine',
            'Szpital': 'masculine',
            'Ogród': 'masculine',
            'Koło': 'neutrum',
            'Obwód': 'masculine'
            }
        predicate2_dict = {
            'masculine': [
                'Organizacyjny', 'Rejestrowy', 'Egzekutywny', 'Wspierający',
                'Transakcyjny', 'Związkowy', 'Zbiorczy'],
            'feminine': [
                'Organizacyjna', 'Rejestrowa', 'Egzekutywna', 'Wspierająca',
                'Transakcyjna', 'Związkowa', 'Zbiorcza'],
            'neutrum': [
                'Organizacyjne', 'Rejestrowe', 'Egzekutywne', 'Wspierające',
                'Transakcyjne', 'Związkowe', 'Zbiorcze']
            }

        propername_list = [
            '"Wspiera się"', '"Totuus"', '"Zawsze Razem"', '"W Kupie Siła"',
            '"Al Capone"', '"UKF"', '"Smak Miesiąca"'
            ]

        # FuzzyChoice object

        subject = (FuzzyChoice(noun_list.keys())).fuzz()
        predicate1 = (FuzzyChoice(predicate1_dict[noun_list[subject]])).fuzz()
        predicate2 = (FuzzyChoice(predicate2_dict[noun_list[subject]])).fuzz()
        propername = (FuzzyChoice(propername_list)).fuzz()

        return '{0} {1} {2} {3}'.format(
            predicate1,
            subject,
            predicate2,
            propername
        )

    class Meta:  # pylint: disable=C0111
        model = Organization

    name = factory.fuzzy.FuzzyAttribute(_organization_name)
    address = factory.Faker('address', locale='pl_PL')
    description = factory.Faker('paragraph', locale='pl_PL')
