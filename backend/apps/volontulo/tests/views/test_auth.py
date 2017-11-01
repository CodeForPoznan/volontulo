# -*- coding: utf-8 -*-

"""
.. module:: test_auth
"""
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
        }, follow=True)
        self.assertRedirects(response, '/o', 302, 200)
        self.assertContains(
            response,
            'Rejestracja przebiegła pomyślnie',
        )
        self.assertContains(
            response,
            'Na podany przy rejestracji email został wysłany link '
            'aktywacyjny. Aby w pełni wykorzystać konto należy je aktywować '
            'poprzez kliknięcie linku lub wklejenie go w przeglądarce.'
        )

        self.assertIn('_auth_user_id', self.client.session)
        self.assertEqual(User.objects.all().count(), 1)

    def test_successful_registration(self):
        """Test for attempt of registration for new user."""
        response = self.client.post('/o/register', {
            'email': 'new@example.com',
            'password': '123new',
            'terms_acceptance': True,
        }, follow=True)
        self.assertRedirects(response, '/o', 302, 200)
        self.assertContains(
            response,
            'Rejestracja przebiegła pomyślnie',
        )
        self.assertContains(
            response,
            'Na podany przy rejestracji email został wysłany link '
            'aktywacyjny. Aby w pełni wykorzystać konto należy je aktywować '
            'poprzez kliknięcie linku lub wklejenie go w przeglądarce.'
        )

        self.assertIn('_auth_user_id', self.client.session)
        self.assertEqual(User.objects.all().count(), 1)

    def test__register_authenticated_user(self):
        """Check if authenticated user can access register page."""
        # volunteer user
        common.initialize_empty_volunteer()

        self.client.post('/o/login', {
            'email': 'volunteer1@example.com',
            'password': 'volunteer1',
        })
        response = self.client.get('/o/login', follow=True)

        self.assertRedirects(
            response,
            '/o',
            302,
            200,
        )
        self.assertEqual(len(response.redirect_chain), 1)
        self.assertEqual(
            response.redirect_chain[0],
            ('/o', 302),
        )
        self.assertIn('_auth_user_id', self.client.session)
        self.assertContains(
            response,
            'Jesteś już zalogowany.'
        )


class TestLogin(TestCase):
    """Class responsible for testing user login view."""

    @classmethod
    def setUpTestData(cls):
        """Set up fixtures data for test."""
        # volunteer user
        common.initialize_empty_volunteer()

    def setUp(self):
        """Set up each test."""
        self.client = Client()

    def test__get_login_by_authorized(self):
        """Get login form by authorized user"""
        self.client.post('/o/login', {
            'email': 'volunteer1@example.com',
            'password': 'volunteer1',
        })
        response = self.client.get('/o/login', follow=True)

        self.assertRedirects(
            response,
            '/o',
            302,
            200,
        )
        self.assertEqual(len(response.redirect_chain), 1)
        self.assertEqual(response.redirect_chain[0], ('/o', 302))
        self.assertIn('_auth_user_id', self.client.session)

    def test__post_login_by_anonymous_user(self):
        """Post to login form by anonymous"""
        # incorrect email or password
        form_params = {
            'email': 'whoami@example.com',
            'password': 'volunteer1',
        }
        response = self.client.post(
            '/o/login',
            form_params,
        )
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Nieprawidłowy email lub hasło!")
        form_params = {
            'email': 'volunteer1@example.com',
            'password': 'xxx',
        }
        response = self.client.post(
            '/o/login',
            form_params,
        )
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Nieprawidłowy email lub hasło!")

        # email and password is correct but and user is not active
        user = User.objects.get(email='volunteer1@example.com')
        user.is_active = False
        user.save()

        form_params = {
            'email': 'volunteer1@example.com',
            'password': 'volunteer1',
        }
        response = self.client.post(
            '/o/login',
            form_params,
        )
        self.assertEqual(response.status_code, 200)
        self.assertContains(
            response,
            "Konto jest nieaktywne, skontaktuj się z administratorem."
        )
        self.assertNotIn('_auth_user_id', self.client.session)

        # email and password is correct and user is active
        user.is_active = True
        user.save()
        form_params = {
            'email': 'volunteer1@example.com',
            'password': 'volunteer1',
        }
        response = self.client.post(
            '/o/login',
            form_params,
            follow=True
        )
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Poprawnie zalogowano")
        self.assertRedirects(
            response,
            '/o',
            302,
            200,
        )
        self.assertEqual(len(response.redirect_chain), 1)
        self.assertEqual(response.redirect_chain[0], ('/o', 302))

    def test__post_login_by_authorized_user(self):
        """Post to login form by authorized"""
        self.client.post('/o/login', {
            'email': 'volunteer1@example.com',
            'password': 'volunteer1',
        })
        response = self.client.get('/o/login', follow=True)

        self.assertRedirects(
            response,
            '/o',
            302,
            200,
        )
        self.assertEqual(len(response.redirect_chain), 1)
        self.assertEqual(response.redirect_chain[0], ('/o', 302))


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
        response = self.client.get('/o/logout', follow=True)

        self.assertRedirects(
            response,
            'http://testserver/o/login?next=/o/logout',
            302,
            200,
        )
        self.assertEqual(len(response.redirect_chain), 1)
        self.assertEqual(
            response.redirect_chain[0],
            ('/o/login?next=/o/logout', 302),
        )
        self.assertNotIn('_auth_user_id', self.client.session)

    def test__logged_out_authenticated_user(self):
        """Testing logout view for authenticated user."""
        self.client.post('/o/login', {
            'email': 'volunteer1@example.com',
            'password': 'volunteer1',
        })
        response = self.client.get('/o/logout', follow=True)

        self.assertRedirects(
            response,
            '/o',
            302,
            200,
        )
        self.assertEqual(len(response.redirect_chain), 1)
        self.assertEqual(response.redirect_chain[0], ('/o', 302))
        self.assertContains(
            response,
            "Użytkownik został wylogowany!"
        )
        self.assertNotIn('_auth_user_id', self.client.session)

    def test__login_authenticated_user(self):
        """Check if authenticated user can access login page."""
        self.client.post('/o/login', {
            'email': 'volunteer1@example.com',
            'password': 'volunteer1',
        })
        response = self.client.get('/o/login', follow=True)

        self.assertRedirects(
            response,
            '/o',
            302,
            200,
        )
        self.assertEqual(len(response.redirect_chain), 1)
        self.assertEqual(response.redirect_chain[0], ('/o', 302))
        self.assertIn('_auth_user_id', self.client.session)
        self.assertContains(
            response,
            'Jesteś już zalogowany.'
        )
