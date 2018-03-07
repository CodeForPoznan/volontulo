# -*- coding: utf-8 -*-

"""
.. module:: auth
"""

from django.conf import settings
from django.contrib import auth
from django.contrib import messages
from django.contrib.auth.models import User
from django.db.utils import IntegrityError
from django.shortcuts import redirect
from django.shortcuts import render
from django.views.generic import View

from apps.volontulo.forms import UserForm
from apps.volontulo.lib.email import send_mail
from apps.volontulo.models import UserProfile


def logout(request):
    """Logout view.

    :param request: WSGIRequest instance
    """
    auth.logout(request)
    return redirect(settings.ANGULAR_ROOT)


class Register(View):
    """View responsible for registering new users."""

    @staticmethod
    def get(request, user_form=None):
        """Simple view to render register form.

        :param request: WSGIRequest instance
        :param user_form: UserForm instance
        """
        if request.user.is_authenticated():
            return redirect(settings.ANGULAR_ROOT)

        return render(
            request,
            'auth/login.html',
            {
                'user_form': UserForm() if user_form is None else user_form,
            }
        )

    @classmethod
    def post(cls, request):
        """Method handles creation of new user.

        :param request: WSGIRequest instance
        """
        # validation of register form:
        user_form = UserForm(request.POST)
        if not user_form.is_valid():
            messages.error(
                request,
                'Wprowadzono nieprawidłowy email, hasło lub nie wyrażono '
                'zgody na przetwarzanie danych osobowych.'
            )
            return cls.get(request, user_form)

        username = request.POST.get('email')
        password = request.POST.get('password')

        ctx = {}

        # attempt of new user creation:
        try:
            user = User.objects.create_user(
                username=username,
                email=username,
                password=password,
                is_active=False,
            )
            user.save()
            profile = UserProfile(user=user)
            ctx['uuid'] = profile.uuid
            profile.save()
        except IntegrityError:
            # if attempt failed, because user already exists we need show
            # error message:
            messages.info(
                request,
                'Użytkownik o podanym emailu już istnieje'
            )
            return cls.get(request, user_form)

        # sending email to user:
        send_mail(request, 'registration', [user.email], context=ctx)

        # show info about successful creation of new user and redirect to
        # homepage:
        messages.success(
            request,
            'Rejestracja przebiegła pomyślnie'
        )
        messages.info(
            request,
            'Na podany przy rejestracji email został wysłany link '
            'aktywacyjny. Aby w pełni wykorzystać konto należy je aktywować '
            'poprzez kliknięcie linku lub wklejenie go w przeglądarce.'
        )
        return redirect(settings.ANGULAR_ROOT)


def activate(request, uuid):
    """View responsible for activating user account."""
    try:
        profile = UserProfile.objects.get(uuid=uuid)
        profile.user.is_active = True
        profile.user.save()
        messages.success(
            request,
            """Pomyślnie aktywowałeś użytkownika."""
        )
    except UserProfile.DoesNotExist:
        messages.error(
            request,
            """Brak użytkownika spełniającego wymagane kryteria."""
        )
    return redirect(settings.ANGULAR_ROOT)
