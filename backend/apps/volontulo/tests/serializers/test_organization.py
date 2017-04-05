# -*- coding: utf-8 -*-

"""
.. module:: test_organization
"""

from django.test import TestCase

from apps.volontulo.models import Organization
from apps.volontulo.serializers import OrganizationSerializer


class TestOrganizationSerializer(TestCase):

    """Test for organizations serializer."""

    def test_slug(self):
        """Test slug method."""
        organization = Organization(name='Organization Name 123')
        self.assertEqual(
            OrganizationSerializer().get_slug(organization),
            'organization-name-123',
        )
