from django.test import TestCase
from django.urls import reverse
from rest_framework.test import APITestCase

from apps.volontulo.factories import UserFactory, OrganizationFactory

ENDPOINT_URL = reverse('api_login')


class TestLoginView(APITestCase, TestCase):

    def test_login(self):
        user = UserFactory.create(password='123abcd')
        organization = OrganizationFactory.create()
        organization.userprofiles = [user.userprofile]
        organization.save()

        res = self.client.post(ENDPOINT_URL, {
            'username': user.username,
            'password': '123abcd'
        }, format='json')

        self.assertEqual(res.status_code, 200)
