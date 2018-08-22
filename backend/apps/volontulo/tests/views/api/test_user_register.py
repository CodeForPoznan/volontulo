# -*- coding: utf-8 -*-
"""
.. module:: test_user_register
"""
import json

from django.urls import reverse
from django.test import TestCase

from apps.volontulo.factories import UserFactory


class TestUserRegister(TestCase):
    """ Tests for user register """

    def test_first_registration(self):
        """Test new user's registration"""
        response = self.client.post(
            reverse('register'),
            json.dumps({
                "email": "jannowak@o2.pl",
                "password": "jan123456"
            }),
            content_type='application/json'
        )
        self.assertEqual(response.status_code, 201)

    def test_second_registration(self):
        """Test register if user is registered already"""
        UserFactory.create(
            email="volunteer2@example.com",
            password="volunteer2",
        )
        response = self.client.post(
            reverse('register'),
            json.dumps({
                "email": "volunteer2@example.com",
                "password": "volunteer2"
            }),
            content_type='application/json'
        )
        self.assertEqual(response.status_code, 201)
