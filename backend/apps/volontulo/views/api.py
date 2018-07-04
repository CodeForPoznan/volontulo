# -*- coding: utf-8 -*-
# pylint: disable=no-self-use

"""
.. module:: api
"""

from django.contrib import messages
from django.contrib.auth import authenticate, get_user_model
from django.contrib.auth import login
from django.contrib.auth import logout
from django.contrib.auth.models import User
from django.contrib.auth.tokens import default_token_generator
from django.contrib.messages import get_messages
from django.contrib.sites.shortcuts import get_current_site
from django.core.exceptions import ValidationError
from django.db.models import Q
from django.db.utils import IntegrityError
from django.shortcuts import get_object_or_404
from django.utils.encoding import force_bytes, force_text
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import status
from rest_framework.decorators import api_view, detail_route
from rest_framework.decorators import authentication_classes
from rest_framework.decorators import permission_classes
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework import viewsets
from rest_framework.views import APIView

from apps.volontulo import models
from apps.volontulo import permissions
from apps.volontulo import serializers
from apps.volontulo.authentication import CsrfExemptSessionAuthentication
from apps.volontulo.lib.email import send_mail
from apps.volontulo.models import Organization
from apps.volontulo.models import UserProfile
from apps.volontulo.serializers import (
    OrganizationContactSerializer, UsernameSerializer, PasswordSerializer,
    ContactSerializer, PasswordChangeSerializer,
)
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
            serializers.UserSerializer(user).data,
            status=status.HTTP_200_OK,
        )

    return Response(
        serializers.UserSerializer(request.user).data,
        status=status.HTTP_400_BAD_REQUEST,
    )


@api_view(['POST'])
@authentication_classes((CsrfExemptSessionAuthentication,))
@permission_classes((AllowAny,))
def register_view(request):
    """REST API register view."""
    if request.user.is_authenticated():
        return Response(status=status.HTTP_400_BAD_REQUEST)

    email = request.data.get('email')
    password = request.data.get('password')

    user = User.objects.create_user(
        username=email,
        email=email,
        password=password,
        is_active=False,
    )
    try:
        user.save()
    except IntegrityError:
        return Response(status=status.HTTP_201_CREATED)

    profile = UserProfile(user=user)
    ctx = {'token': profile.uuid}
    profile.save()
    send_mail(request, 'registration', [user.email], context=ctx)

    return Response(status=status.HTTP_201_CREATED)


@api_view(['POST'])
@authentication_classes((CsrfExemptSessionAuthentication,))
@permission_classes((AllowAny,))
def activate_view(_, uuid):
    """View responsible for activating user account."""
    try:
        profile = UserProfile.objects.get(uuid=uuid)
    except (UserProfile.DoesNotExist, ValidationError):
        return Response(status=status.HTTP_404_NOT_FOUND)

    if profile.user.is_active:
        return Response(status=status.HTTP_400_BAD_REQUEST)
    profile.user.is_active = True
    profile.user.save()
    return Response(status=status.HTTP_201_CREATED)


@api_view(['POST'])
@permission_classes((AllowAny,))
def logout_view(request):
    """REST API logout view."""
    if request.user.is_authenticated():
        logout(request)
        messages.success(request, 'Wylogowano')
        return Response({}, status=status.HTTP_200_OK)
    return Response({}, status=status.HTTP_400_BAD_REQUEST)


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


@authentication_classes((CsrfExemptSessionAuthentication,))
@api_view(['GET'])
@permission_classes((AllowAny,))
def messages_view(request):
    """REST API view with Django messages."""
    return Response(
        serializers.MessageSerializer(get_messages(request), many=True).data,
        status=status.HTTP_200_OK
    )


@authentication_classes((CsrfExemptSessionAuthentication,))
class OfferViewSet(viewsets.ModelViewSet):

    """REST API offers viewset."""

    queryset = models.Offer.objects.order_by('weight')
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
        qs = super(OfferViewSet, self).get_queryset()

        if logged_as_admin(self.request):
            return qs
        user = self.request.user
        if user.is_authenticated():
            return qs.filter(
                Q(offer_status='published') |
                Q(organization__in=user.userprofile.organizations.all())
            )
        return qs.filter(offer_status='published')


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


class Contact(APIView):
    """Get all contact-related info and send contact message to admin."""
    permission_classes = (AllowAny, )

    def get(self, request):  # pylint: disable=unused-argument
        """Return emails of administrators and possible contact entities."""
        query = get_user_model().objects.filter(
            userprofile__is_administrator=True,
        ).order_by('email')
        return Response({
            'administrator_emails': list(
                query.values_list('email', flat=True)
            ),
            'applicant_types': ContactSerializer.APPLICANT_CHOICES,
        }, status.HTTP_200_OK)

    def post(self, request):
        """Sends contact email."""
        serializer = ContactSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        data = serializer.validated_data

        admin = User.objects.get(email=data['administrator_email'])
        # For now send the same message to both user and administrator
        send_mail(
            request,
            'contact_to_admin',
            [
                admin.email,
                data['applicant_email'],
            ],
            data,
            send_copy_to_admin=False,
        )
        return Response({}, status.HTTP_201_CREATED)


class CurrentUser(APIView):
    """REST API view for current user."""
    permission_classes = (IsAuthenticated, )

    def get(self, request):
        """Gets current user."""
        return Response(
            serializers.UserSerializer(request.user).data,
            status=status.HTTP_200_OK,
        )

    def post(self, request):
        """Updates current user."""
        serializer = serializers.UserSerializer(
            request.user, data=request.data,
        )
        if serializer.is_valid(raise_exception=True):
            user = serializer.save()
            return Response(
                serializers.UserSerializer(user).data,
                status=status.HTTP_200_OK,
            )


class PasswordChangeView(APIView):
    """Password change view."""
    permission_classes = (IsAuthenticated,)
    authentication_classes = (CsrfExemptSessionAuthentication,)

    @staticmethod
    def post(request):
        """Changes password of logged in user."""
        user = request.user  # type: User
        serializer = PasswordChangeSerializer(
            data=request.data,
            context={'user': request.user},
        )
        serializer.is_valid(raise_exception=True)
        data = serializer.validated_data

        user.set_password(data['password_new'])
        user.save()
        return Response({}, status.HTTP_200_OK)
