# -*- coding: utf-8 -*-

"""
.. module:: test_pages
"""
from django.test import Client
from django.test import TestCase

from apps.volontulo.tests import common


class TestPages(TestCase):
    """Class responsible for testing various pages."""

    @classmethod
    def setUpTestData(cls):
        """Set up data for all tests."""
        common.initialize_filled_volunteer_and_organization()
        common.initialize_administrator()

    def setUp(self):
        """Set up each test."""
        self.client = Client()

    def test__homepage_for_anonymous(self):
        """Home page for anonymous users."""
        response = self.client.get('/o')
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'homepage.html')
        self.assertIn('offers', response.context)
        self.assertEqual(len(response.context['offers']), 4)

    def test__homepage_for_volunteer_and_organization(self):
        """Home page for volunteers and organizations.

        There's currently no difference for anonymous
        or volunteer/organization - for now.
        """
        response = self.client.get('/o')
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'homepage.html')
        self.assertIn('offers', response.context)
        self.assertEqual(len(response.context['offers']), 4)

    def test__homepage_for_administrator(self):
        """Home page for administrators."""
        self.client.post('/o/login', {
            'email': 'admin_user@example.com',
            'password': 'admin_password',
        })
        response = self.client.get('/o')
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'homepage.html')
        self.assertIn('offers', response.context)
        self.assertEqual(len(response.context['offers']), 10)

        offers = {'NEW': 0, 'ACTIVE': 0, 'SUSPENDED': 0}
        for offer in response.context['offers']:
            offers[offer.status_old] += 1

        self.assertEqual(offers['ACTIVE'], 0)
        self.assertEqual(offers['NEW'], 5)
        self.assertEqual(offers['SUSPENDED'], 5)

    def test__get_organization_faq_staticpage(self):
        """Organization FAQ static page"""
        response = self.client.get('/o/pages/faq-organizations')
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'pages/faq-organizations.html')
        self.assertContains(response, 'Często zadawane pytania')

    def test__get_volunteer_faq_staticpage(self):
        """Volunteer FAQ static page"""
        response = self.client.get('/o/pages/faq-volunteers')
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'pages/faq-volunteers.html')
        self.assertContains(response, 'Często zadawane pytania')

    def test_office_subpage(self):
        """Test office subpage."""
        response = self.client.get('/o/office')
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'pages/office.html')
        self.assertContains(response,
                            'Dyżury dla wolontariuszy oraz organizacji')
