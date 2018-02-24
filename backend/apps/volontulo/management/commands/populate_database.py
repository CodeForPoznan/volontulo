# -*- coding: utf-8 -*-

import random

from django.core.management.base import BaseCommand

from apps.volontulo.factories import OfferFactory
from apps.volontulo.factories import OrganizationFactory
from apps.volontulo.factories import UserProfileFactory
from apps.volontulo.models import Offer
from apps.volontulo.models import Organization


class Command(BaseCommand):
    """Populate database with fake items."""

    help = "Populates database with fake items."

    def handle(self, *args, **options):
        """Populate database with fake objects."""

        # create 5 organizations:
        for _ in range(5):
            organization = OrganizationFactory.create()
            UserProfileFactory.create(
                organizations=(organization,),
            )

        # create 50 offers:
        for _ in range(50):
            OfferFactory.create(
                organization=random.choice(Organization.objects.all())
            )

        # create 150 volunteers:
        for _ in range(150):
            userprofile = UserProfileFactory.create()
            no_of_offers = random.randrange(10)
            for offer in random.sample(
                list(Offer.objects.all()), no_of_offers
            ):
                offer.volunteers.add(userprofile.user)

        self.stdout.write(
            self.style.SUCCESS('Database successfully populated')
        )
