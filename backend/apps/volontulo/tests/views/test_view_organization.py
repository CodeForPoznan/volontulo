# -*- coding: utf-8 -*-

"""
.. module:: test_view_organization
"""
from django.core import mail

from apps.volontulo.tests.views.test_organizations import TestOrganizations


class TestCreateOrganization(TestOrganizations):
    """Class responsible for testing editing organization specific views."""

    def test__get_empty_organization_view_by_anonymous(self):
        """Request for empty organization view by anonymous user."""
        response = self.client.get('/o/organizations/organization-1/{}'.format(
            self.organization.id
        ))

        self.assertEqual(response.status_code, 200)
        self.assertIn('contact_form', response.context)
        self.assertIn('offers', response.context)
        self.assertIn('organization', response.context)
        self.assertContains(response, 'Nazwa')
        self.assertContains(response, 'Opis')
        self.assertContains(response, 'Adres')
        self.assertContains(response, 'Formularz kontaktowy')
        self.assertContains(
            response,
            'Ta organizacja nie utworzyła jeszcze żadnych ofert.'
        )
        self.assertTemplateUsed(
            response,
            'organizations/organization_view.html'
        )
        self.assertTemplateUsed(response, 'contact_form.html')
        self.assertContains(response, 'Wyślij')

    def test__get_filled_organization_view_by_anonymous(self):
        """Request for filled organization view by anonymous user."""
        response = self.client.get('/o/organizations/organization-2/{}'.format(
            self.organization2.id
        ))

        self.assertNotContains(
            response,
            'Ta organizacja nie utworzyła jeszcze żadnych ofert.'
        )
        self.assertIn('offers', response.context)
        self.assertEqual(len(response.context['offers']), 14)

    def test__get_empty_organization_view_by_volunteer(self):
        """Requesting for empty organization view by volunteer user."""
        self.client.login(
            username='volunteer2@example.com',
            password='volunteer2',
        )
        response = self.client.get('/o/organizations/organization-1/{}'.format(
            self.organization.id
        ))

        self.assertContains(response, 'Organization 1')
        self.assertIn('allow_edit', response.context)
        self.assertFalse(response.context['allow_edit'])
        self.assertNotContains(response, 'Edytuj organizację')
        self.assertIn('allow_offer_create', response.context)
        self.assertFalse(response.context['allow_offer_create'])
        self.assertNotContains(response, 'Dodaj ofertę')

    def test__get_empty_organization_view_by_organization(self):
        """Request for empty organization view by organization user."""
        self.client.login(
            username='organization1@example.com',
            password='organization1',
        )
        response = self.client.get(
            '/o/organizations/organization-1/{}'.format(self.organization.id),
            follow=True
        )
        self.assertIn('allow_contact', response.context)
        self.assertIn('allow_edit', response.context)
        self.assertIn('allow_offer_create', response.context)
        self.assertFalse(response.context['allow_contact'])
        self.assertTrue(response.context['allow_edit'])
        self.assertTrue(response.context['allow_offer_create'])
        self.assertContains(response, 'Edytuj organizację')
        self.assertContains(response, 'Dodaj ofertę')

        self.client.login(
            username='organization2@example.com',
            password='organization2',
        )
        response = self.client.get(
            '/o/organizations/organization-1/{}'.format(self.organization.id),
            follow=True
        )
        self.assertNotContains(response, 'Edytuj organizację')
        self.assertNotContains(response, 'Dodaj ofertę')
        self.assertIn('allow_contact', response.context)
        self.assertTrue(response.context['allow_contact'])
        self.assertFalse(response.context['allow_edit'])
        self.assertFalse(response.context['allow_offer_create'])

    def test__get_filled_organization_view_by_organization(self):
        """Request for filled organization view by organization user."""
        self.client.login(
            username='organization2@example.com',
            password='organization2',
        )
        response = self.client.get(
            '/o/organizations/organization-2/{}'.format(self.organization2.id),
            follow=True
        )
        self.assertIn('offers', response.context)
        self.assertEqual(len(response.context['offers']), 14)

    def test__post_contact_form_on_organization_view_by_anonymous(self):
        """Post contact form to organization view by anonymous user."""
        form_params = {
            'name': '',
            'email': '',
            'phone_no': '',
            'message': '',
        }
        response = self.client.post(
            '/o/organizations/organization-1/{}'.format(self.organization.id),
            form_params,
            follow=True
        )

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Formularz zawiera nieprawidłowe dane")

        form_params = {
            'name': 'Mister Volunteer',
            'email': 'mister.volunteer@example.com',
            'phone_no': '+48 123 123 123',
            'message': '',
        }
        response = self.client.post(
            '/o/organizations/organization-1/{}'.format(self.organization.id),
            form_params,
            follow=True
        )

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Formularz zawiera nieprawidłowe dane')
        self.assertContains(response, 'Mister Volunteer')
        self.assertContains(response, '+48 123 123 123')
        self.assertContains(response, 'mister.volunteer@example.com')

        form_params = {
            'name': '',
            'email': '',
            'phone_no': '',
            'message': 'Wiadomość dla organizacji',
        }
        response = self.client.post(
            '/o/organizations/organization-1/{}'.format(self.organization.id),
            form_params,
            follow=True
        )
        self.assertContains(response, 'Wiadomość dla organizacji')
        self.assertEqual(len(mail.outbox), 0)

    def test__post_contact_form_on_organization_view_by_volunteer(self):
        """Post contact form to organization view by volunteer user."""
        self.client.login(
            username='volunteer1@example.com',
            password='volunteer1',
        )
        form_params = {
            'name': '',
            'email': '',
            'phone_no': '',
            'message': '',
            'organization': 1,
        }
        response = self.client.post(
            '/o/organizations/organization-2/{}'.format(self.organization2.id),
            form_params,
            follow=True
        )
        self.assertContains(response, 'Formularz zawiera nieprawidłowe dane')

        form_params = {
            'name': 'Mister volunteer',
            'email': 'mister.volunteer@example.com',
            'phone_no': '+48 123 123 123',
            'message': 'To jest wiadomość dla organizacji od wolontariusza',
            'organization': 1,
        }
        response = self.client.post(
            '/o/organizations/organization-2/{}'.format(self.organization2.id),
            form_params
        )
        self.assertEqual(len(mail.outbox), 1)
        self.assertEqual(mail.outbox[0].subject, 'Kontakt od wolontariusza')
        self.assertContains(
            response,
            'Email został wysłany.'
        )

    def test__post_contact_form_on_organization_view_by_organization(self):
        """Post contact form to organization view by organization user."""
        self.client.login(
            username='organization2@example.com',
            password='organization2',
        )
        form_params = {
            'name': 'Mister volunteer',
            'email': 'mister.volunteer@example.com',
            'phone_no': '+48 123 123 123',
            'message': 'To jest wiadomość dla organizacji od wolontariusza',
            'organization': 1,
        }
        response = self.client.post(
            '/o/organizations/organization-1/{}'.format(self.organization.id),
            form_params,
            follow=True
        )

        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(mail.outbox), 1)
        self.assertEqual(mail.outbox[0].subject, 'Kontakt od wolontariusza')
        self.assertContains(
            response,
            'Email został wysłany.'
        )
