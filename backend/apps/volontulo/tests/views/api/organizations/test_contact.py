"""
.. module:: test_contact
"""
import json
from unittest import mock
from django.test import TestCase

from apps.volontulo.factories import OrganizationFactory


class TestOrganizationContact(TestCase):

    """ Tests for organization contact API """

    def setUp(self):
        """ Set up for each test """
        self.org = OrganizationFactory.create()

    def test_404_if_org_does_not_exist(self):
        """ Test for getting an organization """
        res = self.client.post('/api/organizations/999/contact/')
        self.assertEqual(res.status_code, 404)

    def test_400_if_payload_incorrect(self):
        """ Test for sending incorrect payload"""
        res = self.client.post(
            '/api/organizations/{}/contact/'.format(self.org.id),
            json.dumps({
                'name': 'Jon Snow',
                'email': 'iknownothing-winterfell.com',
                'phone_no': '99999',
                'message': 'Winter is comming!'
            }),
            content_type='application/json'
        )
        self.assertEqual(res.status_code, 400)

    def test_405_if_method_not_alowed(self):
        """ Test for using wrong method """
        res = self.client.get(
            '/api/organizations/{}/contact/'.format(self.org.id))
        self.assertEqual(res.status_code, 405)

    def test_201(self):
        """ Test for sending correct contact message """
        res = self.client.post(
            '/api/organizations/{}/contact/'.format(self.org.id),
            json.dumps({
                'name': 'Jon Snow',
                'email': 'iknownothing@winterfell.com',
                'phone_no': '999999999',
                'message': 'Winter is comming!'
            }),
            content_type='application/json'
        )
        self.assertEqual(res.status_code, 201)

    def test_send_email(self):
        """ Test for sending email """
        with mock.patch('apps.volontulo.views.api.send_mail') as mock_send:
            res = self.client.post(
                '/api/organizations/{}/contact/'.format(self.org.id),
                json.dumps({
                    'name': 'Jon Snow',
                    'email': 'iknownothing@winterfell.com',
                    'phone_no': '999999999',
                    'message': 'Winter is comming!'
                }),
                content_type='application/json'
            )

        self.assertEqual(res.status_code, 201)
        self.assertEqual(mock_send.call_count, 1)
