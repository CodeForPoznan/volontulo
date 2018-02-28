# -*- coding: utf-8 -*-

"""
.. module:: test_create_organization
"""

from django.conf import settings

from apps.volontulo.tests.views.test_organizations import TestOrganizations
from apps.volontulo.models import Organization


class TestCreateOrganization(TestOrganizations):
    """Class responsible for testing editing organization specific views."""

    def test__create_organization_get_form_anonymous(self):
        """Test getting form for creating organization as anonymous."""
        # Disable for anonymous user
        response = self.client.get('/o/organizations/create')

        self.assertEqual(response.status_code, 302)
        self.assertRedirects(
            response,
            '{}/login?next=http%3A//testserver/o/organizations/create'.format(
                settings.ANGULAR_ROOT,
            ),
            302,
            fetch_redirect_response=False,
        )

    def test__create_organization_get_form_authorized(self):
        """Test getting form for creating organization as authorized."""
        self.client.login(
            username='volunteer1@example.com',
            password='volunteer1',
        )
        response = self.client.get('/o/organizations/create')

        self.assertTemplateUsed(
            response,
            'organizations/organization_form.html'
        )
        self.assertIn('organization', response.context)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Tworzenie organizacji')

    def test__create_organization_post_form_anonymous(self):
        """Test posting form for creating organization as anonymous."""
        # Disable for anonymous user
        response = self.client.post('/o/organizations/create')

        self.assertEqual(response.status_code, 302)
        self.assertRedirects(
            response,
            '{}/login?next=http%3A//testserver/o/organizations/create'.format(
                settings.ANGULAR_ROOT,
            ),
            302,
            fetch_redirect_response=False,
        )

    def test__create_empty_organization_post_form(self):
        """Test posting form for creating empty (not filled) organization."""
        self.client.login(
            username='volunteer1@example.com',
            password='volunteer1',
        )
        form_params = {
            'name': '',
            'address': '',
            'description': '',
        }
        response = self.client.post('/o/organizations/create', form_params)

        self.assertIn('organization', response.context)
        self.assertEqual(response.status_code, 200)
        self.assertContains(
            response,
            "Należy wypełnić wszystkie pola formularza."
        )

    def test__create_organization_post_form_fill_fields(self):
        """Test posting form and check fields population."""
        self.client.login(
            username='volunteer1@example.com',
            password='volunteer1',
        )
        form_params = {
            'name': 'Halperin Organix',
            'address': 'East Street 123',
        }
        response = self.client.post('/o/organizations/create', form_params)

        self.assertIn('organization', response.context)
        self.assertEqual(response.status_code, 200)
        self.assertContains(
            response,
            'Halperin Organix'
        )
        self.assertContains(
            response,
            'East Street 123'
        )

        form_params = {
            'description': 'User unfriendly organization',
        }
        response = self.client.post('/o/organizations/create', form_params)
        self.assertIn('organization', response.context)
        self.assertEqual(response.status_code, 200)
        self.assertContains(
            response,
            'User unfriendly organization'
        )

    def test__create_valid_organization_form_post(self):
        """Test posting valid form for creating organization."""
        org_name = 'Halperin Organix'
        self.client.login(
            username='volunteer1@example.com',
            password='volunteer1',
        )
        form_params = {
            'name': org_name,
            'address': 'East Street 123',
            'description': 'User unfriendly organization',
        }
        response = self.client.post(
            '/o/organizations/create',
            form_params,
            follow=True
        )

        self.assertContains(
            response,
            "Organizacja została dodana."
        )
        record = Organization.objects.get(name=org_name)
        self.assertRedirects(
            response,
            'http://testserver/o/organizations/halperin-organix/{}'.format(
                record.id),
            302, 200)
        self.assertEqual(record.name, org_name)
        self.assertEqual(record.address, 'East Street 123')
        self.assertEqual(record.description, 'User unfriendly organization')

    def test__create_organization_one_column_template(self):
        """Test validate one column template on create page."""
        # Disable for anonymous user
        self.client.login(
            username='volunteer1@example.com',
            password='volunteer1',
        )
        response = self.client.get('/o/organizations/create')

        self.assertTemplateUsed(
            response,
            'common/col1.html'
        )
