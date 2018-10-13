"""
.. module:: filters
"""

from rest_framework import filters


class IsOfferJoinedFilter(filters.BaseFilterBackend):

    """Filter offers based on if user joined an offer."""

    def filter_queryset(self, request, queryset, view):
        if request.query_params.get('joined') == 'true':
            if request.user.is_authenticated():
                return queryset.filter(volunteers__in=[request.user])
            return queryset.none()
        elif request.query_params.get('joined') == 'false':
            if request.user.is_authenticated():
                return queryset.exclude(volunteers__in=[request.user])
        return queryset
