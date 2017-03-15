# -*- coding: utf-8 -*-

"""
.. module:: permissions
"""

from rest_framework import permissions


class OfferPermission(permissions.BasePermission):

    """REST API offers' permissions."""

    def has_permission(self, request, view):
        """We are accepting only safe methods for now."""
        return request.method in permissions.SAFE_METHODS


class OrganizationPermission(permissions.BasePermission):

    """REST API organizations' permissions."""

    def has_permission(self, request, view):
        """We are accepting only safe methods for now."""
        return request.method in permissions.SAFE_METHODS
