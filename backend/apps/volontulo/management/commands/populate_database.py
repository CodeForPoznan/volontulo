
import random

from django.contrib.auth.models import User
from django.core.management.base import BaseCommand, CommandError
from django.db import models

from apps.volontulo.factories import (
    UserProfileFactory, UserFactory, OrganizationFactory, OfferFactory
    )
from apps.volontulo.models import Organization, Offer, UserProfile


class Command(BaseCommand):
    """Populate database with fake items."""

    help = "Populates database with fake items."

    def create_list_of_objects(self, type_of_objects, how_many_in_list):
        # creates set of objects (ie. User, Organization, Offer)
        # in order to join them to m2m relation
        if type_of_objects == 'Organization':
            return random.sample(
                list(Organization.objects.all()),
                how_many_in_list
                )
        elif type_of_objects == 'User':
            return random.sample(
                list(User.objects.all()),
                how_many_in_list
                )
        elif type_of_objects == 'Offer':
            return random.sample(
                list(Offer.objects.all()),
                how_many_in_list
                )
        else:
            raise ValueError(
                '{} is not a propper value'.format(type_of_objects)
                )
            return

    def handle(self, *args, **options):
        """Populate database with fake objects."""

        # create 5 organizations
        for organization in range(0, 5):
            OrganizationFactory.create()

        # create admin-user
        UserProfileFactory.create(is_administrator=True)

        # create 15 volunteers
        for volunteer in range(0, 14):
            UserProfileFactory.create(
                organizations=self.create_list_of_objects('Organization', 3),
                is_administrator=False
                )

        # create 50 offers
        for offer in range(0, 50):
            OfferFactory.create(
                organization=self.create_list_of_objects(
                    'Organization', 1
                    )[0],
                volunteers=self.create_list_of_objects('User', 3)
                )

        self.stdout.write(self.style.SUCCESS(
            'Database successfully populated'
            ))
