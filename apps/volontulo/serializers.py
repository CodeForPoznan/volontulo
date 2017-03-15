# -*- coding: utf-8 -*-

"""
.. module:: serializers
"""

from rest_framework import serializers

from apps.volontulo import models


class OfferSerializer(serializers.ModelSerializer):

    """REST API offers' serializer."""

    class Meta:
        model = models.Offer
        fields = '__all__'
