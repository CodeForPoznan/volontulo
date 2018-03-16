# -*- coding: utf-8 -*-

"""
.. module:: serializers
"""

from django.contrib.auth.models import User
from django.utils.text import slugify
from rest_framework import serializers
from rest_framework.fields import CharField, EmailField

from apps.volontulo import models


class OrganizationSerializer(serializers.HyperlinkedModelSerializer):

    """REST API organizations serializer."""

    slug = serializers.SerializerMethodField()

    class Meta:
        model = models.Organization
        fields = (
            'address',
            'description',
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
            'action_status',
            'finished_at',
            'id',
            'image',
            'location',
            'offer_status',
            'organization',
            'slug',
            'started_at',
            'title',
            'url',
            'description',
            'benefits',
            'requirements',
            'time_commitment',
            'time_period',
            'recruitment_end_date',
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
    organizations = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = (
            'is_administrator',
            'organizations',
            'username',
        )

    @staticmethod
    def get_is_administrator(obj):
        """Returns information if user is an administrator."""
        return obj.userprofile.is_administrator

    def get_organizations(self, obj):
        """Returns organizations that user belongs to."""
        qs = obj.userprofile.organizations.all()
        return OrganizationSerializer(qs, many=True, context=self.context).data


# pylint: disable=abstract-method
class OrganizationContactSerializer(serializers.Serializer):
    """Serializer for contact message"""
    name = CharField(required=True, min_length=2, max_length=150,
                     trim_whitespace=True)
    email = EmailField(required=True)
    phone_no = CharField(required=True, min_length=9, max_length=15,
                         trim_whitespace=True)
    message = CharField(required=True, min_length=2, max_length=500,
                        trim_whitespace=True)


# pylint: disable=abstract-method
class UsernameSerializer(serializers.Serializer):
    """Serializer for password reset"""
    username = EmailField(required=True)


# pylint: disable=abstract-method
class PasswordSerializer(serializers.Serializer):
    """Serializer for password reset"""
    password = CharField(required=True, min_length=2, max_length=150)


class MessageSerializer(serializers.Serializer):
    """Serializer for messages from Django contrib."""
    message = CharField(required=True)
    type = CharField(required=True, source='level_tag')
