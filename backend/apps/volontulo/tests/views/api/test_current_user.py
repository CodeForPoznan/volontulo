# pylint:disable=missing-docstring
from django.contrib.auth.models import User
from django.test import TestCase
from django.urls import reverse
from rest_framework.test import APITestCase

from apps.volontulo.factories import UserFactory
from apps.volontulo.serializers import UserSerializer

ENDPOINT_URL = reverse('current_user')


class TestCurrentUserViewGET(APITestCase, TestCase):
    @classmethod
    def setUpClass(cls):
        cls.user = UserFactory.create()

    @classmethod
    def tearDownClass(cls):
        cls.user.delete()

    def test_get_unauthorized(self):
        res = self.client.get(
            ENDPOINT_URL, {}, format='json',
        )

        # Authentication classes are messed up
        # we have to rely on permission classes instead
        # so here we get 403 instead of 401
        self.assertEqual(res.status_code, 403)

    def test_get(self):
        self.client.force_login(self.user)
        res = self.client.get(ENDPOINT_URL, {}, format='json')

        self.assertDictEqual(res.data, UserSerializer(self.user).data)


class TestCurrentUserViewPOST(APITestCase, TestCase):
    @classmethod
    def setUpClass(cls):
        cls.user = UserFactory.create()

    @classmethod
    def tearDownClass(cls):
        cls.user.delete()

    def test_post_uauthorized(self):
        res = self.client.get(
            ENDPOINT_URL, {}, format='json',
        )

        # Authentication classes are messed up
        # we have to rely on permission classes instead
        # so here we get 403 instead of 401
        self.assertEqual(res.status_code, 403)

    def test_post_malformed(self):
        self.client.force_login(self.user)
        res = self.client.post(
            ENDPOINT_URL,
            {
                'first_name': 'X',
                'last_name': '50',
                'phone_no': '1' * 33,
                'is_administrator': True,
            },
            format='json',
        )

        self.assertEqual(res.status_code, 400)
        self.assertDictEqual(
            res.data,
            {
                'last_name': [
                    'Upewnij się, że pole ma co najmniej 3 znaków.',
                ],
                'first_name': [
                    'Upewnij się, że pole ma co najmniej 3 znaków.',
                ],
                'phone_no': [
                    'Upewnij się, że to pole ma nie więcej niż 32 znaków.',
                ]
            },
        )

    def test_post_read_only(self):
        self.client.force_login(self.user)
        user_before = UserSerializer(self.user).data
        res = self.client.post(
            ENDPOINT_URL,
            {
                'email': 'X',
                'is_administrator': True,
                'organizations': [1],
                'username': 'Mikey X',
            },
            format='json',
        )

        self.assertEqual(res.status_code, 200)
        self.assertDictEqual(res.data, user_before)

    def test_post(self):
        self.client.force_login(self.user)
        user_before = UserSerializer(self.user).data

        res = self.client.post(
            ENDPOINT_URL,
            {
                'first_name': 'Mikey',
                'last_name': 'Melnik',
                'phone_no': '600 900 100',
            },
            format='json',
        )

        self.assertEqual(res.status_code, 200)
        self.assertDictEqual(
            res.data,
            UserSerializer(User.objects.get(id=self.user.id)).data,
        )
        self.assertNotEqual(res.data['first_name'], user_before['first_name'])
        self.assertNotEqual(res.data['last_name'], user_before['last_name'])
        self.assertNotEqual(res.data['phone_no'], user_before['phone_no'])
