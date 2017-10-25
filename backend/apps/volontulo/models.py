# -*- coding: utf-8 -*-

"""
.. module:: models
"""

import logging
import os
import uuid

from django.conf import settings
from django.contrib.auth.models import User
from django.db import models
from django.db.models import F
from django.utils import timezone

logger = logging.getLogger('volontulo.models')


class Organization(models.Model):
    """Model that handles ogranizations/institutions."""
    name = models.CharField(max_length=150)
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
            offer_status='published',
            action_status__in=('ongoing', 'future'),
            recruitment_status__in=('open', 'supplemental'),
        ).all()

    def get_for_administrator(self):
        """Return all offers for administrator to allow management."""
        return self.filter(offer_status='unpublished').all()

    def get_weightened(self):
        """Return all published offers ordered by weight."""
        return self.filter(offer_status='published').order_by('weight')

    def get_archived(self):
        """Return archived offers."""
        return self.filter(
            offer_status='published',
            action_status__in=('ongoing', 'finished'),
            recruitment_status='closed',
        ).all()


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
    ACTION_STATUSES = (
        ('future', 'Future'),
        ('ongoing', 'Ongoing'),
        ('finished', 'Finished'),
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
    status_old = models.CharField(
        max_length=30,
        default='NEW',
        null=True,
        unique=False
    )
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
    action_status = models.CharField(
        max_length=16,
        choices=ACTION_STATUSES,
        default='ongoing',
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
    weight = models.IntegerField(default=0, null=True, blank=True)

    def __str__(self):
        """Offer string representation."""
        return self.title

    def set_main_image(self, is_main):
        """Set main image flag unsetting other offers images.

        :param is_main: Boolean flag resetting offer main image
        """
        if is_main:
            OfferImage.objects.filter(offer=self).update(is_main=False)
            return True
        return False

    def save_offer_image(self, gallery, is_main=False):
        """Handle image upload for user profile page.

        :param gallery: UserProfile model instance
        :param userprofile: UserProfile model instance
        :param is_main: Boolean main image flag
        """
        gallery.offer = self
        gallery.is_main = self.set_main_image(is_main)
        gallery.save()
        return self

    def create_new(self):
        """Set status while creating new offer."""
        self.offer_status = 'unpublished'
        self.recruitment_status = 'open'

        if self.started_at or self.finished_at:
            self.action_status = self.determine_action_status()

    def determine_action_status(self):
        """Determine action status by offer dates."""
        if (
                (
                    self.finished_at and
                    self.started_at < timezone.now() < self.finished_at
                ) or
                (
                    self.started_at < timezone.now() and
                    not self.finished_at
                )
        ):
            return 'ongoing'
        if self.started_at > timezone.now():
            return 'future'
        return 'finished'

    def change_status(self, status):
        """Change offer status.

        :param status: string Offer status
        """
        if status in ('published', 'rejected', 'unpublished'):
            self.offer_status = status
            self.save()
        return self

    def unpublish(self):
        """Unpublish offer."""
        self.offer_status = 'unpublished'
        self.save()
        return self

    def publish(self):
        """Publish offer."""
        self.offer_status = 'published'
        Offer.objects.all().update(weight=F('weight') + 1)
        self.weight = 0
        self.save()
        return self

    def reject(self):
        """Reject offer."""
        self.offer_status = 'rejected'
        self.save()
        return self

    def close_offer(self):
        """Change offer status to close."""
        self.offer_status = 'unpublished'
        self.action_status = 'finished'
        self.recruitment_status = 'closed'
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

    def is_admin(self):
        """Return True if current user is administrator, else return False"""
        return self.is_administrator

    def is_in_organization(self):
        """Return True if current user is in any organization"""
        return self.organizations.exists()

    def is_volunteer(self):
        """Return True if current user is volunteer, else return False"""
        return not (self.is_administrator and self.organizations)

    def can_edit_offer(self, offer=None, offer_id=None):
        """Checks if the user can edit an offer based on its ID"""
        if offer is None:
            offer = Offer.objects.get(id=offer_id)
        return self.is_administrator or self.organizations.filter(
            id=offer.organization_id).exists()

    def get_avatar(self):
        """Return avatar for current user."""
        return UserGallery.objects.filter(
            userprofile=self,
            is_avatar=True
        )

    def clean_images(self):
        """Clean user images."""
        images = UserGallery.objects.filter(userprofile=self)
        for image in images:
            try:
                os.remove(os.path.join(settings.MEDIA_ROOT, str(image.image)))
            except OSError as ex:
                logger.error(ex)

            image.delete()

    def __str__(self):
        return self.user.email


def uuid_image_name(prefix):
    """Upload to function decorator.

    Prefix is a directory, that file will be saved in.
    """
    def upload_to(_, filename):
        """Actual uload_to function, that use prefix from outer scope."""
        _, file_extension = os.path.splitext(filename)
        return os.path.join(
            prefix,
            '{}{}'.format(uuid.uuid4(), file_extension),
        )
    return upload_to


class UserGallery(models.Model):
    """Handling user images."""
    userprofile = models.ForeignKey(UserProfile, related_name='images')
    image = models.ImageField(upload_to=uuid_image_name('profiles'))
    is_avatar = models.BooleanField(default=False)

    def __str__(self):
        """String representation of an image."""
        return str(self.image)


class OfferImage(models.Model):
    """Handling offer image."""
    offer = models.ForeignKey(Offer, related_name='images')
    path = models.ImageField(upload_to=uuid_image_name('offers'))
    is_main = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        """String representation of an image."""
        return str(self.path)


class Page(models.Model):
    """Static page model."""

    title = models.CharField(max_length=255)
    content = models.TextField()
    author = models.ForeignKey(UserProfile)
    published = models.BooleanField(default=False)
    modified_at = models.DateTimeField(auto_now=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title
