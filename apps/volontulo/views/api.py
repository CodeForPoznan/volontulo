# -*- coding: utf-8 -*-

"""
.. module:: api
"""

from django.contrib.auth import models as auth_models
from rest_framework import viewsets

from apps.volontulo import models
from apps.volontulo import permissions
from apps.volontulo import serializers
from apps.volontulo.views import logged_as_admin


class OfferViewSet(viewsets.ModelViewSet):

    """REST API offers' viewset."""

    serializer_class = serializers.OfferSerializer
    permission_classes = (permissions.OfferPermission,)

    def get_queryset(self):
        """Queryset depends on user role."""
        if logged_as_admin(self.request):
            return models.Offer.objects.get_for_administrator()
        return models.Offer.objects.get_weightened()


class OrganizationViewSet(viewsets.ModelViewSet):

    """REST API organizations' viewset."""

    queryset = models.Organization.objects.all()
    serializer_class = serializers.OrganizationSerializer
    permission_classes = (permissions.OrganizationPermission,)


class UserViewSet(viewsets.ModelViewSet):

    """REST API users' viewset."""

    queryset = auth_models.User.objects.all()
    serializer_class = serializers.UserSerializer
