from unittest.mock import patch

from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.test import TestCase
from django.urls import reverse
from rest_framework.test import APITestCase

from apps.volontulo.factories import UserFactory

ENDPOINT_URL = reverse('password_change')


class TestPasswordChange(APITestCase, TestCase):

    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.password = 'admin12345'
        cls.user = UserFactory.create()  # type: User
        cls.user.set_password(cls.password)
        cls.user.save()

    def test_403_when_not_authenticated(self):
        res = self.client.post(ENDPOINT_URL, data={}, format='json')

        self.assertEqual(res.status_code, 403)
        self.assertDictEqual(
            res.data,
            {'detail': 'Nie podano danych uwierzytelniających.'},
        )

    def test_new_password_empty(self):
        self.client.force_login(self.user)
        res = self.client.post(
            ENDPOINT_URL,
            {'password_old': self.password, 'password_new': ''},
            format='json',
        )

        self.assertEqual(res.status_code, 400)
        self.assertDictEqual(
            res.data,
            {'password_new': ['To pole nie może być puste.']},
        )

    def test_old_password_invalid(self):
        self.client.force_login(self.user)
        with patch(
            'apps.volontulo.serializers.validate_password',
            side_effect=ValidationError('error'),
        ):
            res = self.client.post(
                ENDPOINT_URL,
                data={
                    'password_old': self.password,
                    'password_new': 'admin123123',
                },
                format='json',
            )

        self.assertEqual(res.status_code, 400)
        self.assertDictEqual(
            res.data,
            {
                'password_old': ['error'],
                'password_new': ['error'],
            },
        )

    def test_old_password_not_matching_user_password(self):
        self.client.force_login(self.user)
        res = self.client.post(
            ENDPOINT_URL,
            {
                'password_old': self.password + '1',
                'password_new': 'admin123123',
            },
            format='json',
        )

        self.assertEqual(res.status_code, 400)
        self.assertDictEqual(
            res.data,
            {'password_old': ['Stare hasło jest niepoprawne.']},
        )

    def test_password_change(self, ):
        self.client.force_login(self.user)
        new_password = 'qwerty12345'
        res = self.client.post(
            ENDPOINT_URL,
            {
                'password_old': self.password,
                'password_new': new_password,
            },
            format='json',
        )

        self.assertEqual(res.status_code, 200)
        self.assertTrue(
            User.objects.get(id=self.user.id).check_password(new_password),
        )
