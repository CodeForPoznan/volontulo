# -*- coding: utf-8 -*-

"""
.. module:: serializers
"""

import base64
import io

from dateutil import parser
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.utils.text import slugify
from rest_framework import serializers
from rest_framework.exceptions import PermissionDenied
from rest_framework.fields import CharField, EmailField, ChoiceField

from apps.volontulo import models
from apps.volontulo.validators import validate_admin_email


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

    def create(self, validated_data):
        """Adds created organization to user's organizations list"""
        org = super(OrganizationSerializer, self).create(validated_data)
        org.userprofiles.add(self.context['request'].user.userprofile)
        return org


class OrganizationField(serializers.Field):

    """Custom field for organization serialization."""

    def to_representation(self, value):
        """Transform internal value into serializer representation."""
        return OrganizationSerializer(value, context=self.context).data

    def to_internal_value(self, data):
        """Transform  serializer representation into internal value."""
        try:
            return models.Organization.objects.get(pk=data['id'])
        except (TypeError, KeyError):
            raise serializers.ValidationError(
                "Wartość organizacji ma zły format. "
                "Użyj obiektu z atrybutem id organizacji."
            )


class OfferImageField(serializers.Field):

    """Custom field for offer's image serialization."""

    def to_representation(self, value):
        """Transform internal value into serializer representation."""
        image = (
            value.filter(is_main=True).first() or
            value.first()
        )
        return self.context['request'].build_absolute_uri(
            location=image.path.url
        ) if image else None

    def to_internal_value(self, data):
        """Transform  serializer representation into internal value."""
        data['content'] = base64.b64decode(data['content'])
        return data


class OfferSerializer(serializers.HyperlinkedModelSerializer):

    """REST API offers serializer."""

    start_finish_error = """Data rozpoczęcia akcji nie może być
        późniejsza, niż data zakończenia"""
    recruitment_error = """Data rozpoczęcia rekrutacji
        nie może być późniejsza, niż data zakończenia"""
    reserve_recruitment_error = """Data rozpoczęcia rekrutacji
        rezerwowej nie może być późniejsza, niż data zakończenia"""
    recruitment_start_finish_error = """Rekrutacja rezerwowa
        nie może zacząć się przed podstawową"""

    slug = serializers.SerializerMethodField()
    image = OfferImageField(source='images', allow_null=True, required=False)
    organization = OrganizationField()

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
            'recruitment_start_date',
            'reserve_recruitment',
            'reserve_recruitment_start_date',
            'reserve_recruitment_end_date',
            'action_ongoing',
            'constant_coop',
            'volunteers_limit',
            'reserve_volunteers_limit',
        )
    date_fields = [
        'started_at',
        'finished_at',
        'recruitment_end_date',
        'recruitment_start_date',
        'reserve_recruitment_start_date',
        'reserve_recruitment_end_date'
    ]
    start_finish_error = (
        "Data rozpoczęcia akcji nie może być "
        "późniejsza, niż data zakończenia"
    )
    recruitment_error = (
        "Data rozpoczęcia rekrutacji "
        "nie może być późniejsza, niż data zakończenia"
    )
    reserve_recruitment_error = (
        "Data rozpoczęcia rekrutacji "
        "rezerwowej nie może być późniejsza, niż data zakończenia"
    )

    def to_internal_value(self, data):
        for field in self.date_fields:
            if data.get(field):
                try:
                    data[field] = str(parser.parse(data[field]))
                except (ValueError, TypeError):
                    raise ValidationError(
                        [field, "improper format"], code=None)
        return super().to_internal_value(data)

    def validate(self, attrs):
        data = super(OfferSerializer, self).validate(attrs)
        self._validate_start_finish(data, 'started_at', 'finished_at',
                                    self.start_finish_error)
        self._validate_start_finish(data, 'recruitment_start_date',
                                    'recruitment_end_date',
                                    self.recruitment_error)
        self._validate_start_finish(data, 'reserve_recruitment_start_date',
                                    'reserve_recruitment_end_date',
                                    self.reserve_recruitment_error)
        self._validate_start_finish(data, 'recruitment_start_date',
                                    'reserve_recruitment_start_date',
                                    self.recruitment_start_finish_error)
        return data

    def validate_organization(self, organization):
        """Custom organization validation."""
        userprofile = self.context['request'].user.userprofile
        if (
                organization in userprofile.organizations.all() or
                (userprofile.is_administrator and self.instance is not None)
        ):
            return organization
        raise PermissionDenied(
            detail="Nie posiadasz uprawnień do organizacji."
        )

    @staticmethod
    def _validate_start_finish(data, start_slug, end_slug, error_desc):
        """Validation for date fields."""
        start_field_value = data.get(start_slug)
        end_field_value = data.get(end_slug)
        if start_field_value and end_field_value:
            if start_field_value > end_field_value:
                raise serializers.ValidationError(error_desc)

    def save(self, **kwargs):
        image_set = 'images' in self.validated_data
        if image_set:
            image = self.validated_data.pop('images')

        instance = super(OfferSerializer, self).save(**kwargs)

        if image_set:
            instance.images.all().delete()
            if image:
                instance_image = models.OfferImage(
                    offer=instance,
                    is_main=True,
                )
                instance_image.path.save(
                    image['filename'],
                    io.BytesIO(image['content'])
                )
                instance_image.save()
        return instance

    @staticmethod
    def get_slug(obj):
        """Returns slugified title."""
        return slugify(obj.title)


class UserSerializer(serializers.ModelSerializer):

    """REST API organizations serializer."""

    is_administrator = serializers.SerializerMethodField()
    organizations = serializers.SerializerMethodField()
    phone_no = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = (
            'first_name',
            'last_name',
            'phone_no',
            'email',
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

    @staticmethod
    def get_phone_no(obj):
        """Returns user's phone number."""
        return obj.userprofile.phone_no


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


class ContactSerializer(serializers.Serializer):
    """Serializer for contact message."""
    VOLUNTEER = 'volunteer'
    ORGANIZATION = 'organization'
    APPLICANT_CHOICES = (VOLUNTEER, ORGANIZATION)

    applicant_type = ChoiceField(APPLICANT_CHOICES, required=True)
    applicant_email = EmailField(required=True, max_length=150)
    applicant_name = CharField(required=True, min_length=3, max_length=150)
    administrator_email = EmailField(
        required=True,
        validators=[validate_admin_email],
    )
    message = CharField(required=True, min_length=10, max_length=2000)
    phone_no = CharField(max_length=20)
