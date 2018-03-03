# -*- coding: utf-8 -*-

"""
.. module:: test_auth
"""

from django.conf import settings
from django.contrib.auth.models import User
from django.test import Client
from django.test import TestCase
from django.test import TransactionTestCase

from apps.volontulo.tests import common


class TestRegister(TransactionTestCase):
    """Tests for register view."""

    def setUp(self):
        """Set up each test."""
        self.client = Client()

    def test_get_method(self):
        """Test for get method for view."""
        response = self.client.get('/o/register')
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'auth/login.html')
        self.assertContains(
            response,
            'Rejestracja w Volontulo'
        )
        self.assertContains(
            response,
            'Logowanie'
        )
        self.assertNotIn('_auth_user_id', self.client.session)

    def test_invalid_form(self):
        """Test for post method with invalid form."""
        response = self.client.post('/o/register', {})
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'auth/login.html')
        self.assertContains(
            response,
            'Wprowadzono nieprawidłowy email, hasło lub nie wyrażono '
            'zgody na przetwarzanie danych osobowych.',
        )
        self.assertNotIn('_auth_user_id', self.client.session)

    def test_user_already_exists(self):
        """Test for attempt of registration for user, that already exists."""
        User.objects.create_user(
            'existing@example.com',
            'existing@example.com',
            '123existing'
        )
        response = self.client.post('/o/register', {
            'email': 'existing@example.com',
            'password': '123existing',
            'terms_acceptance': True,
        })
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'auth/login.html')
        self.assertContains(
            response,
            'Użytkownik o podanym emailu już istnieje',
        )
        self.assertNotIn('_auth_user_id', self.client.session)
        self.assertEqual(User.objects.all().count(), 1)

    def test_register_without_term_acceptance(self):
        """Test for registration without accepted terms."""
        response = self.client.post('/o/register', {
            'email': 'notacceptregistration@example.com',
            'password': '123notacceptregistration',
            'terms_acceptance': False,
        })
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'auth/login.html')
        self.assertContains(
            response,
            'Wprowadzono nieprawidłowy email, hasło lub nie wyrażono '
            'zgody na przetwarzanie danych osobowych.',
        )
        self.assertNotIn('_auth_user_id', self.client.session)

    def test_register_with_term_acceptance(self):
        """Test for registration with accepted terms."""
        response = self.client.post('/o/register', {
            'email': 'acceptterms@example.com',
            'password': '123acceptterms',
            'terms_acceptance': True,
        })
        self.assertRedirects(
            response,
            settings.ANGULAR_ROOT,
            302,
            fetch_redirect_response=False,
        )
        self.assertEqual(User.objects.all().count(), 1)

    def test_successful_registration(self):
        """Test for attempt of registration for new user."""
        response = self.client.post('/o/register', {
            'email': 'new@example.com',
            'password': '123new',
            'terms_acceptance': True,
        })
        self.assertRedirects(
            response,
            settings.ANGULAR_ROOT,
            302,
            fetch_redirect_response=False,
        )
        self.assertEqual(User.objects.all().count(), 1)

    def test__register_authenticated_user(self):
        """Check if authenticated user can access register page."""
        # volunteer user
        common.initialize_empty_volunteer()

        self.client.login(
            username='volunteer1@example.com',
            password='volunteer1',
        )
        response = self.client.get('/o/register')

        self.assertRedirects(
            response,
            settings.ANGULAR_ROOT,
            302,
            fetch_redirect_response=False,
        )


class TestLogout(TestCase):
    """Class responsible for testing user logout view."""

    @classmethod
    def setUpTestData(cls):
        """Set up fixtures data for test."""
        # volunteer user
        common.initialize_empty_volunteer()

    def setUp(self):
        """Set up each test."""
        self.client = Client()

    def test__logged_out_anonymous_user(self):
        """Testing logout view for anonymous user"""
        response = self.client.get('/o/logout')
        self.assertRedirects(
            response,
            settings.ANGULAR_ROOT,
            302,
            fetch_redirect_response=False,
        )

    def test__logged_out_authenticated_user(self):
        """Testing logout view for authenticated user."""
        self.client.login(
            username='volunteer1@example.com',
            password='volunteer1',
        )
        response = self.client.get('/o/logout')

        self.assertRedirects(
            response,
            settings.ANGULAR_ROOT,
            302,
            fetch_redirect_response=False,
        )
