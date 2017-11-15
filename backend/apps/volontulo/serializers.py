# -*- coding: utf-8 -*-

"""
.. module:: serializers
"""

from django.contrib.auth.models import User
from django.utils.text import slugify
from rest_framework import serializers

from apps.volontulo import models


class OrganizationSerializer(serializers.HyperlinkedModelSerializer):

    """REST API organizations serializer."""

    slug = serializers.SerializerMethodField()

    class Meta:
        model = models.Organization
        fields = (
            'id',
            'name',
            'slug',
            'url',
        )

    @staticmethod
    def get_slug(obj):
        """Returns slugified name."""
        return slugify(obj.name)


class OfferSerializer(serializers.HyperlinkedModelSerializer):

    """REST API offers serializer."""

    slug = serializers.SerializerMethodField()
    image = serializers.SerializerMethodField()
    organization = OrganizationSerializer(many=False, read_only=True)

    class Meta:
        model = models.Offer
        fields = (
            'finished_at',
            'id',
            'image',
            'location',
            'organization',
            'slug',
            'started_at',
            'title',
            'url',
        )

    def get_image(self, obj):
        """Returns main image's url for an offer."""
        image = (
            obj.images.filter(is_main=True).first() or
            obj.images.first()
        )
        return self.context['request'].build_absolute_uri(
            location=image.path.url
        ) if image else None

    @staticmethod
    def get_slug(obj):
        """Returns slugified title."""
        return slugify(obj.title)


class UserSerializer(serializers.ModelSerializer):

    """REST API organizations serializer."""

    is_administrator = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = (
            'is_administrator',
            'username',
        )

    @staticmethod
    def get_is_administrator(obj):
        """Returns information if user is an administrator."""
        return obj.userprofile.is_administrator
