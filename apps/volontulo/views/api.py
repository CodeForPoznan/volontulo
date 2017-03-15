# -*- coding: utf-8 -*-

"""
.. module:: api
"""

from rest_framework import viewsets

from apps.volontulo import models
from apps.volontulo import serializers


class OfferViewSet(viewsets.ModelViewSet):

    """REST API offers' viewset."""

    queryset = models.Offer.objects.all()
    serializer_class = serializers.OfferSerializer
