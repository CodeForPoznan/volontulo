# -*- coding: utf-8 -*-

import random

from django.core.management.base import BaseCommand
from factory.django import ImageField
from tqdm import tqdm

from apps.volontulo.factories import OfferFactory
from apps.volontulo.factories import OrganizationFactory
from apps.volontulo.factories import placeimg_com_download
from apps.volontulo.factories import UserProfileFactory
from apps.volontulo.models import Offer
from apps.volontulo.models import Organization


class Command(BaseCommand):
    """Populate database with fake items."""

    help = "Populates database with fake items."

    def handle(self, *args, **options):
        """Populate database with fake objects."""

        self.stdout.write(self.style.SUCCESS('Creating 15 organizations'))
        for _ in tqdm(range(15)):
            organization = OrganizationFactory.create()
            UserProfileFactory.create(
                organizations=(organization,),
            )

        self.stdout.write(self.style.SUCCESS('Creating 50 offers'))
        for _ in tqdm(range(50)):
            OfferFactory.create(
                organization=random.choice(Organization.objects.all()),
                image=ImageField(
                    from_func=placeimg_com_download(1000, 400, 'any')
                )
            )

        self.stdout.write(self.style.SUCCESS('Creating 150 volunteers'))
        for _ in tqdm(range(150)):
            userprofile = UserProfileFactory.create()
            no_of_offers = random.randrange(10)
            for offer in random.sample(
                list(Offer.objects.all()), no_of_offers
            ):
                offer.volunteers.add(userprofile.user)

        self.stdout.write(
            self.style.SUCCESS('Database successfully populated')
        )
