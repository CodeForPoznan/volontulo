# -*- coding: utf-8 -*-

"""
.. module:: test_login_view
"""

from django.test import TestCase
from django.urls import reverse
from rest_framework.test import APITestCase

from apps.volontulo.factories import UserFactory

ENDPOINT_URL = reverse('api_logout')


class TestLogoutViewAuthenticated(APITestCase, TestCase):

    def test_logout(self):
        self.client.force_login(UserFactory())
        res = self.client.post(ENDPOINT_URL)
        self.assertEqual(res.status_code, 200)


class TestLogoutViewNotAuthenticated(APITestCase, TestCase):

    def test_logout(self):
        res = self.client.post(ENDPOINT_URL)
        self.assertEqual(res.status_code, 400)
