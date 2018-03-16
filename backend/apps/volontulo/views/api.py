# -*- coding: utf-8 -*-

"""
.. module:: api
"""
from django.contrib import messages
from django.contrib.auth import authenticate
from django.contrib.auth import login
from django.contrib.auth import logout
from django.contrib.auth.models import User
from django.contrib.auth.tokens import default_token_generator
from django.contrib.messages import get_messages
from django.contrib.sites.shortcuts import get_current_site
from django.shortcuts import get_object_or_404
from django.utils.encoding import force_bytes, force_text
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import status
from rest_framework.decorators import api_view, detail_route
from rest_framework.decorators import authentication_classes
from rest_framework.decorators import permission_classes
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework import viewsets

from apps.volontulo import models
from apps.volontulo import permissions
from apps.volontulo import serializers
from apps.volontulo.authentication import CsrfExemptSessionAuthentication
from apps.volontulo.lib.email import send_mail
from apps.volontulo.models import Organization
from apps.volontulo.serializers import \
    OrganizationContactSerializer, UsernameSerializer, PasswordSerializer
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
            return Response(None, status=status.HTTP_401_UNAUTHORIZED)

        login(request, user)

        return Response(
            serializers.UserSerializer(user, context={
                'request': request
            }).data,
            status=status.HTTP_200_OK,
        )

    return Response(
        serializers.UserSerializer(request.user, context={
            'request': request
        }).data,
        status=status.HTTP_400_BAD_REQUEST,
    )


@api_view(['POST'])
@permission_classes((AllowAny,))
def logout_view(request):
    """REST API logout view."""
    if request.user.is_authenticated():
        logout(request)
        messages.success(request, 'Wylogowano')
        return Response({}, status=status.HTTP_200_OK)
    return Response({}, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET'])
@permission_classes((AllowAny,))
def current_user(request):
    """REST API view for current user."""
    if request.user.is_authenticated():
        return Response(
            serializers.UserSerializer(request.user, context={
                'request': request
            }).data,
            status=status.HTTP_200_OK,
        )

    return Response({}, status=status.HTTP_200_OK)


@api_view(['POST'])
@authentication_classes((CsrfExemptSessionAuthentication,))
@permission_classes((AllowAny,))
def password_reset(request):
    """REST API reset password view"""
    serializer = UsernameSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)
    username = serializer.validated_data.get('username')
    try:
        user = User.objects.get(username=username)
    except User.DoesNotExist:
        pass
    else:
        context = {
            'email': username,
            'domain': get_current_site(request).domain,
            'uid': urlsafe_base64_encode(force_bytes(user.pk)),
            'user': user,
            'token': default_token_generator.make_token(user),
            'protocol': 'https' if request.is_secure() else 'http',
        }
        send_mail(
            request,
            'password_reset',
            [username],
            context=context,
            send_copy_to_admin=False)
    return Response(dict(), status=status.HTTP_201_CREATED)


@api_view(['POST'])
@authentication_classes((CsrfExemptSessionAuthentication,))
@permission_classes((AllowAny,))
def password_reset_confirm(request, uidb64, token):
    """REST API reset password confirm"""
    serializer = PasswordSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)
    uid = force_text(urlsafe_base64_decode(uidb64))
    try:
        user = User.objects.get(pk=uid)
    except User.DoesNotExist:
        user = None
    if user is not None and default_token_generator.check_token(user, token):
        user.set_password(serializer.validated_data.get('password'))
        user.save()
    return Response({}, status=status.HTTP_201_CREATED)


@api_view(['GET'])
@permission_classes((AllowAny,))
def messages_view(request):
    """REST API view with Django messages."""
    return Response(
        serializers.MessageSerializer(get_messages(request), many=True).data,
        status=status.HTTP_200_OK
    )


class OfferViewSet(viewsets.ModelViewSet):

    """REST API offers viewset."""

    serializer_class = serializers.OfferSerializer
    permission_classes = (permissions.OfferPermission,)
    filter_backends = (DjangoFilterBackend,)
    filter_fields = (
        'finished_at',
        'location',
        'organization',
        'organization__id',
        'organization__name',
        'requirements',
        'started_at',
        'recruitment_end_date'
        )

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

    @staticmethod
    @detail_route(methods=['POST'], permission_classes=(AllowAny,))
    # pylint: disable=invalid-name
    def contact(request, pk):
        """Endpoint to send contact message to organization"""
        org = get_object_or_404(Organization, id=pk)
        serializer = OrganizationContactSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        send_mail(
            request,
            'volunteer_to_organisation',
            [
                user_profile.user.email
                for user_profile in org.userprofiles.all()
            ],
            serializer.validated_data,
        )
        return Response({}, status=status.HTTP_201_CREATED)

    @staticmethod
    @detail_route(methods=['GET'], permission_classes=(AllowAny,))
    # pylint: disable=invalid-name
    def offers(request, pk):
        """ Endpoint to get offers for organization """
        organization = get_object_or_404(Organization, id=pk)
        is_user_org_member = False
        if request.user.is_authenticated:
            if organization in request.user.userprofile.organizations.all():
                is_user_org_member = True
        if logged_as_admin(request) or is_user_org_member:
            offers = organization.offer_set.get_for_administrator()
        else:
            offers = organization.offer_set.get_weightened()
        return Response(
            serializers.OfferSerializer(
                offers,
                many=True,
                context={'request': request}).data,
            status=status.HTTP_200_OK)
