# -*- coding: utf-8 -*-

"""
.. module:: api
"""

from django.contrib.auth import authenticate
from django.contrib.auth import login
from rest_framework.decorators import api_view
from rest_framework.decorators import authentication_classes
from rest_framework.decorators import permission_classes
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework import viewsets

from apps.volontulo import models
from apps.volontulo import permissions
from apps.volontulo import serializers
from apps.volontulo.authentication import CsrfExemptSessionAuthentication
from apps.volontulo.views import logged_as_admin


@api_view(['POST'])
@authentication_classes((CsrfExemptSessionAuthentication,))
@permission_classes((AllowAny,))
def login_view(request):
    """REST API login view."""
    if not request.user.is_authenticated():
        username = request.data.get('username')
        password = request.data.get('password')
        user = authenticate(username=username, password=password)

        if user is None or not user.is_active:
            return Response({
                'success': False,
                'user': None,
            })

        login(request, user)

    return Response({
        'success': True,
        'user': serializers.UserSerializer(request.user).data,
    })


class OfferViewSet(viewsets.ModelViewSet):

    """REST API offers viewset."""

    serializer_class = serializers.OfferSerializer
    permission_classes = (permissions.OfferPermission,)

    def get_queryset(self):
        """Queryset depends on user role."""
        if logged_as_admin(self.request):
            return models.Offer.objects.get_for_administrator()
        return models.Offer.objects.get_weightened()


class OrganizationViewSet(viewsets.ModelViewSet):

    """REST API organizations viewset."""

    queryset = models.Organization.objects.all()
    serializer_class = serializers.OrganizationSerializer
    permission_classes = (permissions.OrganizationPermission,)
