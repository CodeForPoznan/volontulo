# -*- coding: utf-8 -*-

from django.contrib.auth.models import User
from django.core.management.base import BaseCommand
from django.db.utils import IntegrityError

from apps.volontulo.models import UserProfile


class Command(BaseCommand):
    """Create Volontulo admin."""

    help = "Create Volontulo admin."

    def add_arguments(self, parser):
        parser.add_argument('username', type=str)
        parser.add_argument('password', type=str)
        parser.add_argument(
            '--django-admin',
            action='store_true',
            dest='django_admin',
        )

    def handle(self, *args, **options):
        """Create Volontulo admin."""
        try:
            user = User.objects.create_user(
                username=options['username'],
                email=options['username'],
                password=options['password'],
                is_superuser=options['django_admin'],
                is_staff=options['django_admin'],
                is_active=True,
            )
        except IntegrityError:
            self.stdout.write(self.style.ERROR('User already exists'))
        else:
            user.save()
            UserProfile(
                user=user,
                is_administrator=True,
            ).save()
            self.stdout.write(self.style.SUCCESS('User successfully created'))
