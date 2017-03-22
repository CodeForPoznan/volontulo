# -*- coding: utf-8 -*-

"""
.. module:: test_list
"""

from io import BytesIO

from rest_framework import status
from rest_framework.test import APITestCase
from djangorestframework_camel_case.parser import CamelCaseJSONParser

from apps.volontulo.tests.views.offers.commons import TestOffersCommons


class _TestOrganizationsListAPIView(TestOffersCommons, APITestCase):

    """Tests for REST API's list organizations view."""

    def test_organization_list_fields(self):
        """Test list's fields of organization REST API endpoint."""
        response = self.client.get('/api/organizations/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        # dirty hack intead of checking response.data because of issue
        # djangorestframework-camel-case #26:
        for organization in CamelCaseJSONParser().parse(
                BytesIO(response.content)):
            self.assertIsInstance(organization.pop('id'), int)
            self.assertIsInstance(organization.pop('name'), str)
            self.assertIsInstance(organization.pop('slug'), str)
            self.assertIsInstance(organization.pop('url'), str)
            self.assertEqual(len(organization), 0)


class TestAdminUserOrganizationsListAPIView(_TestOrganizationsListAPIView):

    """Tests for REST API's list organizations view for admin user."""

    def setUp(self):
        """Set up each test."""
        super(TestAdminUserOrganizationsListAPIView, self).setUp()
        self.client.login(username='admin@example.com', password='123admin')

    def test_organization_list_length(self):
        """Test organizations' list length for admin user.

        Organizations are readable for everyone.
        """
        response = self.client.get('/api/organizations/')

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)


class TestOrganizationUserOrganizationsListAPIView(
        _TestOrganizationsListAPIView):

    """Tests for API's list organizations view for user with organization."""

    def setUp(self):
        """Set up each test."""
        super(TestOrganizationUserOrganizationsListAPIView, self).setUp()
        self.client.login(
            username='cls.organization@example.com',
            password='123org'
        )

    def test_organization_list_length(self):
        """Test organizations' list length for user with organization.

        Organizations are readable for everyone.
        """
        response = self.client.get('/api/organizations/')

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)


class TestRegularUserOrganizationsListAPIView(_TestOrganizationsListAPIView):

    """Tests for REST API's list organizations view for regular user."""

    def setUp(self):
        """Set up each test."""
        super(TestRegularUserOrganizationsListAPIView, self).setUp()
        self.client.login(
            username='volunteer@example.com',
            password='123volunteer'
        )

    def test_organization_list_length(self):
        """Test organizations' list length for regular user.

        Organizations are readable for everyone.
        """
        response = self.client.get('/api/organizations/')

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)


class TestAnonymousUserOrganizationsListAPIView(_TestOrganizationsListAPIView):

    """Tests for REST API's list organizations view for anonymous user."""

    def test_organization_list_length(self):
        """Test organizations' list length for anonymous user.

        Organizations are readable for everyone.
        """
        response = self.client.get('/api/organizations/')

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
