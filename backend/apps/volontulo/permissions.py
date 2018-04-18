# -*- coding: utf-8 -*-

"""
.. module:: permissions
"""

from rest_framework import permissions


class OfferPermission(permissions.BasePermission):

    """REST API offers permissions."""

    def has_permission(self, request, view):
        """We are accepting only safe methods for now."""
        return request.method in permissions.SAFE_METHODS or (
            request.method in ('POST', 'PUT') and
            request.user.is_authenticated()
        )

    def has_object_permission(self, request, view, obj):
        user = request.user
        return request.method in permissions.SAFE_METHODS or (
            user.is_authenticated() and (
                user.userprofile.is_administrator or
                obj.organization in user.userprofile.organizations.all()
            )
        )


class OrganizationPermission(permissions.BasePermission):

    """REST API organizations permissions."""

    def has_permission(self, request, view):
        """We are accepting safe methods, post an put methods only for
        authenticated users """
        return request.method in permissions.SAFE_METHODS or (
            request.method in ('POST', 'PUT') and
            request.user.is_authenticated()
        )

    def has_object_permission(self, request, view, obj):
        user = request.user
        return request.method in permissions.SAFE_METHODS or (
            user.is_authenticated() and (
                user.userprofile.is_administrator or
                obj in user.userprofile.organizations.all()
            )
        )
