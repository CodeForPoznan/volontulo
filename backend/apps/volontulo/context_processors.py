# -*- coding: utf-8 -*-

"""
.. module:: authentication
"""

from django.conf import settings


def angular_root(_):
    """Make the ANGULAR_ROOT var available in django templates."""
    return {'ANGULAR_ROOT': settings.ANGULAR_ROOT}
