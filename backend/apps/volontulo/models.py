# -*- coding: utf-8 -*-

"""
.. module:: models
"""

import logging
import os
import uuid

from django.contrib.auth.models import User
from django.db import models
from django.db.models import F
from django.db.models import Q
from django.utils import timezone

logger = logging.getLogger('volontulo.models')


def upload_to_offers(_, filename):
    """
    Upload to offers path.

    This needs to be a full-body func because
    migrations requires it to be serializable.
    """
    _, file_extension = os.path.splitext(filename)
    return os.path.join(
        'offers',
        '{}{}'.format(uuid.uuid4(), file_extension),
    )


class Organization(models.Model):
    """Model that handles ogranizations/institutions."""
    name = models.CharField(max_length=150, db_index=True)
    address = models.CharField(max_length=150)
    description = models.TextField()

    def __str__(self):
        """Organization model string reprezentation."""
        return self.name


class OffersManager(models.Manager):
    """Offers Manager."""

    def get_active(self):
        """Return active offers."""
        return self.filter(
            # that covers action_status__in=('ongoing', 'future'):
            Q(finished_at__isnull=True) | Q(finished_at__gte=timezone.now()),
            offer_status='published',
            recruitment_status__in=('open', 'supplemental'),
        ).all()

    def get_for_administrator(self):
        """Return all offers for administrator to allow management."""
        return self.all()

    def get_weightened(self):
        """Return all published offers ordered by weight."""
        return self.filter(offer_status='published').order_by('weight')


class Offer(models.Model):
    """Offer model."""

    OFFER_STATUSES = (
        ('unpublished', 'Unpublished'),
        ('published', 'Published'),
        ('rejected', 'Rejected'),
    )
    RECRUITMENT_STATUSES = (
        ('open', 'Open'),
        ('supplemental', 'Supplemental'),
        ('closed', 'Closed'),
    )

    objects = OffersManager()
    organization = models.ForeignKey(Organization)
    volunteers = models.ManyToManyField(User)
    description = models.TextField()
    requirements = models.TextField(blank=True, default='')
    time_commitment = models.TextField()
    benefits = models.TextField()
    location = models.CharField(max_length=150)
    title = models.CharField(max_length=150)
    started_at = models.DateTimeField(blank=True, null=True)
    finished_at = models.DateTimeField(blank=True, null=True)
    time_period = models.CharField(max_length=150, default='', blank=True)
    offer_status = models.CharField(
        max_length=16,
        choices=OFFER_STATUSES,
        default='unpublished',
    )
    recruitment_status = models.CharField(
        max_length=16,
        choices=RECRUITMENT_STATUSES,
        default='open',
    )
    votes = models.BooleanField(default=0)
    recruitment_start_date = models.DateTimeField(blank=True, null=True)
    recruitment_end_date = models.DateTimeField(blank=True, null=True)
    reserve_recruitment = models.BooleanField(blank=True, default=True)
    reserve_recruitment_start_date = models.DateTimeField(
        blank=True,
        null=True
    )
    reserve_recruitment_end_date = models.DateTimeField(
        blank=True,
        null=True
    )
    action_ongoing = models.BooleanField(default=False, blank=True)
    constant_coop = models.BooleanField(default=False, blank=True)
    action_start_date = models.DateTimeField(blank=True, null=True)
    action_end_date = models.DateTimeField(blank=True, null=True)
    volunteers_limit = models.IntegerField(default=0, null=True, blank=True)
    reserve_volunteers_limit = models.IntegerField(
        default=0, null=True, blank=True)
    weight = models.IntegerField(default=0, null=True, blank=True)
    image = models.ImageField(
        upload_to=upload_to_offers,
        null=True,
        blank=True
    )

    def __str__(self):
        """Offer string representation."""
        return self.title

    def create_new(self):
        """Set status while creating new offer."""
        self.offer_status = 'unpublished'
        self.recruitment_status = 'open'

    @property
    def action_status(self):
        """Determine action status by offer dates."""
        now = timezone.now()

        if self.started_at and self.started_at > now:
            return 'future'
        if self.finished_at and self.finished_at < now:
            return 'finished'
        return 'ongoing'

    def publish(self):
        """Publish offer."""
        self.offer_status = 'published'
        Offer.objects.all().update(weight=F('weight') + 1)
        self.weight = 0
        self.save()
        return self


class UserProfile(models.Model):
    """Model that handles users profiles."""

    user = models.OneToOneField(User)
    organizations = models.ManyToManyField(
        Organization,
        related_name='userprofiles',
    )
    is_administrator = models.BooleanField(default=False, blank=True)
    phone_no = models.CharField(
        max_length=32,
        blank=True,
        default='',
        null=True
    )
    uuid = models.UUIDField(default=uuid.uuid4, unique=True)

    def is_in_organization(self):
        """Return True if current user is in any organization"""
        return self.organizations.exists()

    def __str__(self):
        return self.user.email
