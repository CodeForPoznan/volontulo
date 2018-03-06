# -*- coding: utf-8 -*-

"""
.. module:: admin
"""

from django.contrib import admin

from apps.volontulo.models import Offer
from apps.volontulo.models import OfferImage
from apps.volontulo.models import Organization
from apps.volontulo.models import UserProfile


admin.site.register(Offer)
admin.site.register(OfferImage)
admin.site.register(Organization)
admin.site.register(UserProfile)
