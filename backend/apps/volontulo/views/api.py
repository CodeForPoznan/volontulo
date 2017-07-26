# -*- coding: utf-8 -*-

"""
.. module:: api
"""

from django.contrib.auth import authenticate, login
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import viewsets

from apps.volontulo import models
from apps.volontulo import permissions
from apps.volontulo import serializers
from apps.volontulo.authentication import CsrfExemptSessionAuthentication
from apps.volontulo.views import logged_as_admin


class LoginView(APIView):
    """
    REST Login view
    """
    authentication_classes = (CsrfExemptSessionAuthentication,)
    permission_classes = ()

    def post(self, request):
        """POST from login"""
        content = {
            'success': False,
            'message': 'User is logged'
        }
        if not request.user.is_authenticated():
            username = request.data.get('username')
            password = request.data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                if user.is_active:
                    login(request, user)
                    content = {
                        'success': True,
                        'message': 'Login success',
                        'username': username
                    }
                else:
                    content = {
                        'success': False,
                        'message': 'User is inactive'
                    }
            else:
                content = {
                    'success': False,
                    'message': 'Incorrect credentials'
                }
        return Response(content)


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
