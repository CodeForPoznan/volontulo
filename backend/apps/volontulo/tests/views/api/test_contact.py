from unittest import mock

from django.test import TestCase
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from apps.volontulo.factories import UserFactory
from apps.volontulo.serializers import ContactSerializer

ENDPOINT_URL = reverse('contact')


class TestContactViewGET(TestCase):

    def test_get(self):
        for _ in range(5):
            UserFactory.create()

        admin_emails = sorted(
            UserFactory.create(userprofile__is_administrator=True).email
            for _ in range(2)
        )

        res = self.client.get(ENDPOINT_URL)

        self.assertDictEqual(res.data, {
            'administrator_emails': admin_emails,
            'applicant_types': ContactSerializer.APPLICANT_CHOICES,
        })


class TestContactViewPOST(APITestCase, TestCase):

    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.admin = UserFactory.create(userprofile__is_administrator=True)

    def setUp(self):
        self.payload = {
            'administrator_email': self.admin.email,
            'applicant_email': 'michal.kowalski@wp.pl',
            'applicant_name': 'Michał Kowalski',
            'applicant_type': ContactSerializer.VOLUNTEER,
            'message': 'Chcę zaangażować się w jakąś akcję, ale nie wiem jak.'
                       ' Możecie mi pomóc :)?',
            'phone_no': '+ 00 48 600 700 800',
        }

    def test_missing_fields(self):
        res = self.client.post(ENDPOINT_URL, {}, format='json')

        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(res.data, {
            'administrator_email': ['To pole jest wymagane.'],
            'applicant_email': ['To pole jest wymagane.'],
            'applicant_name': ['To pole jest wymagane.'],
            'applicant_type': ['To pole jest wymagane.'],
            'message': ['To pole jest wymagane.'],
            'phone_no': ['To pole jest wymagane.'],
        })

    def test_min_length(self):
        payload = self.payload.copy()
        payload.update({
            'applicant_name': 'K',
            'message': 'Cześć!'
        })
        res = self.client.post(ENDPOINT_URL, payload, format='json')

        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertDictEqual(res.data, {
            'applicant_name': [
                'Upewnij się, że pole ma co najmniej 3 znaków.',
            ],
            'message': [
                'Upewnij się, że pole ma co najmniej 10 znaków.',
            ],
        })

    def test_max_length(self):
        payload = self.payload.copy()
        payload.update({
            'applicant_email': 'A' * 150 + '@googlemail.com',
            'applicant_name': 'A' * 151,
            'message': 'A' * 2001,
            'phone_no': '6' * 21,
        })
        res = self.client.post(ENDPOINT_URL, payload, format='json')

        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertDictEqual(res.data, {
            'applicant_email': [
                'Upewnij się, że to pole ma nie więcej niż 150 znaków.',
            ],
            'applicant_name': [
                'Upewnij się, że to pole ma nie więcej niż 150 znaków.',
            ],
            'message': [
                'Upewnij się, że to pole ma nie więcej niż 2000 znaków.',
            ],
            'phone_no': [
                'Upewnij się, że to pole ma nie więcej niż 20 znaków.',
            ],
        })

    def test_admin_email_validation(self):
        payload = self.payload.copy()
        payload.update({
            'administrator_email': 'not-really-valid@admin.com',
        })
        res = self.client.post(ENDPOINT_URL, payload, format='json')

        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertDictEqual(res.data, {
            'administrator_email': [
                'Administrator o adresie e-mail'
                ' not-really-valid@admin.com nie istnieje.',
            ],
        })

    def test_applicant_type_validation(self):
        payload = self.payload.copy()
        payload.update({
            'applicant_type': 'president',
        })
        res = self.client.post(ENDPOINT_URL, payload, format='json')

        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertDictEqual(res.data, {
            'applicant_type': [
                '"president" nie jest poprawnym wyborem.',
            ],
        })

    @mock.patch('apps.volontulo.views.api.send_mail')
    def test_email_is_sent(self, mock_send_mail):
        res = self.client.post(ENDPOINT_URL, self.payload, format='json')

        self.assertEqual(res.status_code, status.HTTP_201_CREATED)

        call_args = mock_send_mail.call_args[0]

        self.assertEqual(call_args[1], 'contact_to_admin')
        self.assertEqual(call_args[2], [
            self.payload['administrator_email'],
            self.payload['applicant_email'],
        ])
        self.assertEqual(call_args[3], self.payload)
