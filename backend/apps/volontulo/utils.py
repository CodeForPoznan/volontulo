# -*- coding: utf-8 -*-

"""
.. module:: utils
"""

from django.contrib.auth.models import User
from django.shortcuts import get_object_or_404
from django.shortcuts import redirect
from django.utils.text import slugify

from apps.volontulo.models import UserProfile


# Offers statuses dictionary with meaningful names.
# todo: remove dependency
OFFERS_STATUSES = {
    'NEW': 'Nowa',
    'ACTIVE': 'Aktywna',
    'FINISHED': 'Zakończona',
    'SUSPENDED': 'Zawieszona',
    'CLOSED': 'Zamknięta',
}


def get_administrators_emails():
    """Get all administrators emails or superuser email

    Format returned:
    emails = {
        1: 'admin1@example.com',
        2: 'admin2@example.com',
    }
    """
    administrators = UserProfile.objects.filter(is_administrator=True)
    emails = {}
    for admin in administrators:
        emails[str(admin.user.id)] = admin.user.email

    if not emails:
        administrators = User.objects.filter(is_superuser=True)
        for admin in administrators:
            emails[str(admin.id)] = admin.email

    return emails


def correct_slug(model_class, view_name, slug_field):
    """Decorator that is reposponsible for redirect to url with correct slug.

    It is used by url for offers, organizations and users.
    """
    def decorator(wrapped_func):
        """Decorator function for correcting slugs."""

        def wrapping_func(request, slug, id_):
            """Wrapping function for correcting slugs."""
            obj = get_object_or_404(model_class, id=id_)
            if slug != slugify(getattr(obj, slug_field)):
                return redirect(
                    view_name,
                    slug=slugify(getattr(obj, slug_field)),
                    id_=id_
                )
            return wrapped_func(request, slug, id_)

        return wrapping_func

    return decorator
