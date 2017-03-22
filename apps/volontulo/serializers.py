# -*- coding: utf-8 -*-

"""
.. module:: serializers
"""

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

    @staticmethod
    def get_slug(obj):
        """Returns slugified name."""
        return slugify(obj.name)
