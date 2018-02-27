"""
.. module:: test_password_reset
"""

import json
from unittest import mock
from django.contrib.auth.tokens import default_token_generator
from django.test import TestCase
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode

from apps.volontulo.factories import UserFactory


class TestPasswordReset(TestCase):

    """ Tests for resetting password API """

    def setUp(self):
        """ Set up for each test """
        self.user = UserFactory.create()
        self.uid = str(
            urlsafe_base64_encode(force_bytes(self.user.pk)),
            'utf-8')
        self.token = default_token_generator.make_token(self.user)

    def test_password_reset_400_bad_request(self):
        """ Test for sending bad request """
        res = self.client.post(
            '/api/password-reset',
            json.dumps({'username': 'You-Know-Who'}),
            content_type='application/json'
        )
        self.assertEqual(res.status_code, 400)

    def test_password_reset_405_if_method_not_allowed(self):
        """ Test for using wrong method """
        res = self.client.get('/api/password-reset')
        self.assertEqual(res.status_code, 405)

    def test_password_reset_415_if_incorrect_format(self):
        """ Test for sending username in incorrect format """
        res = self.client.post(
            '/api/password-reset',
            {'username': 'you_know_who@slytherin.com'}
        )
        self.assertEqual(res.status_code, 415)

    def test_password_reset_201_created(self):
        """ Test for sending username in correct format """
        res = self.client.post(
            '/api/password-reset',
            json.dumps({'username': self.user.username}),
            content_type='application/json'
        )
        self.assertEqual(res.status_code, 201)

    @mock.patch('apps.volontulo.views.api.send_mail')
    def test_send_email(self, mock_send):
        """ Test for sending email """
        res = self.client.post(
            '/api/password-reset',
            json.dumps({'username': self.user.username}),
            content_type='application/json'
        )
        self.assertEqual(res.status_code, 201)
        self.assertEqual(mock_send.call_count, 1)

    def test_password_reset_confirm_400_bad_request(self):
        """ Test for sending incorrect password """
        res = self.client.post(
            '/api/password-reset/{}/{}'.format(self.uid, self.token),
            json.dumps({'password': 'Q'}),
            content_type='application/json'
        )
        self.assertEqual(res.status_code, 400)

    def test_password_reset_confirm_405_if_method_not_allowed(self):
        """ Test for using wrong method """
        res = self.client.get(
            '/api/password-reset/{}/{}'.format(self.uid, self.token)
        )
        self.assertEqual(res.status_code, 405)

    def test_password_reset_confirm_404(self):
        """ Test for page not found  """
        res = self.client.post(
            '/api/password-reset/999',
            json.dumps({'password': 'AvadaKedavra'}),
            content_type='application/json')
        self.assertEqual(res.status_code, 404)

    def test_password_reset_confirm_201_created(self):
        """ Test for sending password in correct format """
        res = self.client.post(
            '/api/password-reset/{}/{}'.format(self.uid, self.token),
            json.dumps({'password': 'AvadaKedavra'}),
            content_type='application/json')
        self.assertEqual(res.status_code, 201)
