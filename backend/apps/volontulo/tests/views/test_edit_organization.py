# -*- coding: utf-8 -*-

"""
.. module:: test_edit_organization
"""

from django.conf import settings

from apps.volontulo.tests.views.test_organizations import TestOrganizations


class TestEditOrganization(TestOrganizations):
    """Class responsible for testing editing organization specific views."""

    def test__edit_organization_get_form_anonymous(self):
        """Get organization edit form as anonymous."""
        response = self.client.get(
            '/o/organizations/organization-1/{}/edit'.format(
                self.organization.id),
        )

        self.assertRedirects(
            response,
            '{}/login?next=http%3A//testserver'
            '/o/organizations/organization-1/{}/edit'.format(
                settings.ANGULAR_ROOT, self.organization.id
            ),
            302,
            fetch_redirect_response=False
        )

    def test__edit_organization_post_form_anonymous(self):
        """Post organization edit form as anonymous."""
        response = self.client.get(
            '/o/organizations/organization-1/{}/edit'.format(
                self.organization.id),
        )

        self.assertRedirects(
            response,
            '{}/login?next=http%3A//testserver'
            '/o/organizations/organization-1/{}/edit'.format(
                settings.ANGULAR_ROOT, self.organization.id
            ),
            302,
            fetch_redirect_response=False
        )

    def test__edit_organization_get_form_volunteer(self):
        """Get organization edit form as volunteer."""
        self.client.login(
            username='volunteer1@example.com',
            password='volunteer1',
        )
        response = self.client.get(
            '/o/organizations/organization-1/{}/edit'.format(
                self.organization.id
            ),
            follow=True,
        )

        self.assertRedirects(
            response,
            '/o/organizations/organization-1/{}'.format(self.organization.id),
            302,
            200,
        )
        self.assertEqual(len(response.redirect_chain), 1)
        self.assertEqual(
            response.redirect_chain[0],
            (
                '/o/organizations/organization-1/{}'.format(
                    self.organization.id
                ),
                302
            ),
        )
        self.assertContains(
            response,
            'Nie masz uprawnień do edycji tej organizacji.'
        )

    def test__edit_organization_post_form_volunteer(self):
        """Post organization edit form as volunteer."""
        self.client.login(
            username='volunteer1@example.com',
            password='volunteer1',
        )
        response = self.client.get(
            '/o/organizations/organization-1/{}/edit'.format(
                self.organization.id
            ),
            follow=True,
        )

        self.assertRedirects(
            response,
            '/o/organizations/organization-1/{}'.format(self.organization.id),
            302,
            200,
        )
        self.assertEqual(len(response.redirect_chain), 1)
        self.assertEqual(
            response.redirect_chain[0],
            (
                '/o/organizations/organization-1/{}'.format(
                    self.organization.id
                ),
                302
            ),
        )
        self.assertContains(
            response,
            'Nie masz uprawnień do edycji tej organizacji.'
        )

    def test__edit_organization_get_form_other_organization(self):
        """Get organization edit form as other organization."""
        self.client.login(
            username='organization2@example.com',
            password='organization2',
        )
        response = self.client.get(
            '/o/organizations/organization-1/{}/edit'.format(
                self.organization.id
            ),
            follow=True,
        )

        self.assertRedirects(
            response,
            '/o/organizations/organization-1/{}'.format(self.organization.id),
            302,
            200,
        )
        self.assertEqual(len(response.redirect_chain), 1)
        self.assertEqual(
            response.redirect_chain[0],
            (
                '/o/organizations/organization-1/{}'.format(
                    self.organization.id
                ),
                302
            ),
        )
        self.assertContains(
            response,
            'Nie masz uprawnień do edycji tej organizacji.'
        )

    def test__edit_organization_post_form_other_organization(self):
        """Post organization edit form as other organization."""
        self.client.login(
            username='organization2@example.com',
            password='organization2',
        )
        response = self.client.get(
            '/o/organizations/organization-1/{}/edit'.format(
                self.organization.id),
            follow=True,
        )

        self.assertRedirects(
            response,
            '/o/organizations/organization-1/{}'.format(self.organization.id),
            302,
            200,
        )
        self.assertEqual(len(response.redirect_chain), 1)
        self.assertEqual(
            response.redirect_chain[0],
            (
                '/o/organizations/organization-1/{}'.format(
                    self.organization.id
                ),
                302
            ),
        )
        self.assertContains(
            response,
            'Nie masz uprawnień do edycji tej organizacji.'
        )

    def test__edit_organization_get_form_right_organization(self):
        """Get organization edit form as right organization."""
        self.client.login(
            username='organization1@example.com',
            password='organization1',
        )
        response = self.client.get(
            '/o/organizations/organization-1/{}/edit'.format(
                self.organization.id
            ),
            follow=True,
        )
        self.assertEqual(response.status_code, 200)
        self.assertIn('organization', response.context)
        self.assertContains(response, 'Nazwa')
        self.assertContains(response, 'Adres')
        self.assertContains(response, 'Opis')
        self.assertContains(response, 'Zapisz zmiany')
        self.assertEqual(
            response.context['organization'].name,
            'Organization 1'
        )
        self.assertEqual(
            response.context['organization'].address,
            'Organization 1 address'
        )
        self.assertEqual(
            response.context['organization'].description,
            'Organization 1 description'
        )

    def test__edit_organization_post_form_right_organization(self):
        """Post organization edit form as right organization."""
        self.client.login(
            username='organization1@example.com',
            password='organization1',
        )
        # not enough data send
        form_params = {
            'name': '',
            'address': '',
            'description': '',
        }
        response = self.client.post(
            '/o/organizations/organization-1/{}/edit'.format(
                self.organization.id),
            form_params,
            follow=True,
        )

        self.assertEqual(response.status_code, 200)
        self.assertContains(
            response,
            "Należy wypełnić wszystkie pola formularza."
        )

        # properly filled form
        form_params = {
            'name': 'New Organization 1 name',
            'address': 'New Organization 1 address',
            'description': 'New Organization 1 description',
        }

        response = self.client.post(
            '/o/organizations/organization-1/{}/edit'.format(
                self.organization.id
            ),
            form_params,
            follow=True,
        )

        self.assertRedirects(
            response,
            '/o/organizations/new-organization-1-name/{}'.format(
                self.organization.id
            ),
            302,
            200,
        )
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Oferta została dodana/zmieniona.')
