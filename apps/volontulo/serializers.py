# -*- coding: utf-8 -*-

"""
.. module:: serializers
"""

from django.contrib.auth import models as auth_models
from django.utils.text import slugify
from rest_framework import serializers

from apps.volontulo import models


class OfferSerializer(serializers.HyperlinkedModelSerializer):

    """REST API offers' serializer."""

    slug = serializers.SerializerMethodField()
    image = serializers.SerializerMethodField()

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
        """Return main image's url for an offer."""
        image = (
            obj.images.filter(is_main=True).first() or
            obj.images.first()
        )
        return self.context['request'].build_absolute_uri(
            location=image.path.url
        ) if image else None

    def get_slug(self, obj):
        return slugify(obj.title)


class OrganizationSerializer(serializers.HyperlinkedModelSerializer):

    """REST API organizations' serializer."""

    slug = serializers.SerializerMethodField()

    class Meta:
        model = models.Organization
        fields = (
            'id',
            'name',
            'slug',
            'url',
        )

    def get_slug(self, obj):
        return slugify(obj.name)


class UserSerializer(serializers.HyperlinkedModelSerializer):

    """REST API users' serializer."""

    class Meta:
        model = auth_models.User
        fields = (
            'email',
            'url',
        )
