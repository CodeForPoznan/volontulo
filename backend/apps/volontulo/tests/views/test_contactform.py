# -*- coding: utf-8 -*-

"""
.. module:: test_contactform
"""
from django.core import mail
from django.test import Client
from django.test import TestCase

from apps.volontulo.tests import common


class TestPages(TestCase):
    """Class responsible for testing contact forms."""

    test_admin_email = test_admin_username = 'admin@admin.com'
    test_admin_password = 'admin_password'

    @classmethod
    def setUpTestData(cls):
        # admin user
        cls.admin = common.initialize_administrator(
            username=cls.test_admin_username, email=cls.test_admin_email,
            password=cls.test_admin_password
        )
        # volunteer user - totally useless
        cls.volunteer = common.initialize_empty_volunteer()
        # organization user - no offers
        common.initialize_empty_organization()
        # volunteer user - offers, organizations
        common.initialize_filled_volunteer_and_organization()

    def setUp(self):
        """Set up each test."""
        self.client = Client()

    def test__get_contact_with_administrator_form_by_anonymous(self):
        """Request contact with administrator form by anonymous user."""
        response = self.client.get('/o/contact', follow=True)

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'contact.html')
        self.assertTemplateUsed(response, 'contact_form.html')
        self.assertContains(response, 'Formularz kontaktowy')
        self.assertIn('contact_form', response.context)

    def test__get_contact_with_administrator_form_by_volunteer(self):
        """Request contact with administrator form by volunteer user."""
        self.client.login(
            username='volunteer1@example.com',
            password='volunteer1',
        )
        response = self.client.get('/o/contact')

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'contact.html')
        self.assertTemplateUsed(response, 'contact_form.html')
        self.assertContains(response, 'Formularz kontaktowy')
        self.assertIn('contact_form', response.context)

    def test__get_contact_with_administrator_form_by_organization(self):
        """Request contact with administrator form by organization user."""
        self.client.login(
            username='organization1@example.com',
            password='organization1',
        )
        response = self.client.get('/o/contact')

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'contact.html')
        self.assertTemplateUsed(response, 'contact_form.html')
        self.assertContains(response, 'Formularz kontaktowy')
        self.assertIn('contact_form', response.context)

    def test__post_contact_with_administrator_form_by_anonymous(self):
        """Post to contact with administrator form by anonymous user."""
        form_params = {
            'applicant': 'VOLUNTEER',
            'administrator': self.admin.id,
            'name': 'John Smith',
            'email': 'john.smith@example.com',
            'phone_no': '+48 123 123 123',
            'message': 'Beautiful is better than ugly.'
        }

        response = self.client.post(
            '/o/contact',
            form_params,
            follow=True
        )

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'contact.html')
        self.assertTemplateUsed(response, 'contact_form.html')
        self.assertContains(response, 'Formularz kontaktowy')
        self.assertIn('contact_form', response.context)
        self.assertEqual(len(mail.outbox), 1)
        self.assertEqual(mail.outbox[0].subject, 'Kontakt z administratorem')
        self.assertContains(response, 'Email został wysłany.')

    def test__contact_with_admin_form_by_volunteer_val_error(self):
        """Post to contact with administrator form by volunteer user assuming
        validation error.
        """
        self.client.login(
            username='volunteer1@example.com',
            password='volunteer1',
        )

        form_params = {
            'applicant': 'VOLUNTEER',
            'administrator': self.admin.id,
            'name': '',
            'email': '',
            'phone_no': '',
            'message': '',
        }
        response = self.client.post(
            '/o/contact',
            form_params,
            follow=True
        )

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'contact.html')
        self.assertTemplateUsed(response, 'contact_form.html')
        self.assertContains(response, 'Formularz kontaktowy')
        self.assertIn('contact_form', response.context)
        self.assertContains(response, 'Proszę poprawić błędy w formularzu:')
        self.assertEqual(len(mail.outbox), 0)

    def test__contact_with_admin_form_by_volunteer(self):
        """Post to contact with administrator form by volunteer user."""
        self.client.login(
            username='volunteer1@example.com',
            password='volunteer1',
        )
        form_params = {
            'applicant': 'VOLUNTEER',
            'administrator': self.admin.id,
            'name': 'Bull Pillman',
            'email': 'pull.billman@example.com',
            'phone_no': '+48 123 123 123',
            'message': 'My crime is that of curiosity.'
        }
        response = self.client.post(
            '/o/contact',
            form_params,
            follow=True
        )

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'contact.html')
        self.assertTemplateUsed(response, 'contact_form.html')
        self.assertContains(response, 'Formularz kontaktowy')
        self.assertIn('contact_form', response.context)
        self.assertEqual(len(mail.outbox), 1)
        self.assertEqual(mail.outbox[0].subject, 'Kontakt z administratorem')
        self.assertContains(response, 'Email został wysłany.')

    def test__contact_with_admin_form_by_organization_val_error(self):
        """Post to contact with administrator form by organization user
        validation error.
        """
        self.client.login(
            username='organization1@example.com',
            password='organization1',
        )
        # incorrect params
        form_params = {
            'applicant': 1,
            'administrator': 1,
            'name': '',
            'email': '',
            'phone_no': '',
            'message': '',
        }
        response = self.client.post(
            '/o/contact',
            form_params,
            follow=True
        )

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'contact.html')
        self.assertTemplateUsed(response, 'contact_form.html')
        self.assertContains(response, 'Formularz kontaktowy')
        self.assertIn('contact_form', response.context)
        self.assertEqual(len(mail.outbox), 0)
        self.assertContains(response, 'Proszę poprawić błędy w formularzu:')

    def test__contact_with_admin_form_by_organization_val_success(self):
        """Post to contact with administrator form by organization user
        validation success.
        """
        self.client.login(
            username=self.admin.email,
            password=self.test_admin_password
        )

        # correct params
        form_params = {
            'applicant': 'ORGANIZATION',
            'administrator': self.admin.id,
            'name': 'Bull Pillman',
            'email': 'pull.billman@example.com',
            'phone_no': '+48 123 123 123',
            'message': 'My crime is that of curiosity.'
        }

        response = self.client.post(
            '/o/contact',
            form_params,
            follow=True
        )

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'contact.html')
        self.assertTemplateUsed(response, 'contact_form.html')
        self.assertContains(response, 'Formularz kontaktowy')
        self.assertIn('contact_form', response.context)
        self.assertEqual(len(mail.outbox), 1)
        self.assertEqual(mail.outbox[0].subject, 'Kontakt z administratorem')
        self.assertContains(response, 'Email został wysłany.')
