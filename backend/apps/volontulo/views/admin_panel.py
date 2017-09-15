# -*- coding: utf-8 -*-

"""
.. module:: admin_panel
"""

from django.shortcuts import redirect
from django.shortcuts import render


def main_panel(request):
    """Main admin panel view."""
    user = request.user
    if not user.is_authenticated() or not user.userprofile.is_administrator:
        return redirect('offers_list')

    return render(
        request,
        'admin/list_offers.html'
    )
