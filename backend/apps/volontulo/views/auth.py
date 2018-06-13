# -*- coding: utf-8 -*-

"""
.. module:: auth
"""

from django.conf import settings
from django.contrib import auth
from django.shortcuts import redirect


def logout(request):
    """Logout view.

    :param request: WSGIRequest instance
    """
    auth.logout(request)
    return redirect(settings.ANGULAR_ROOT)
