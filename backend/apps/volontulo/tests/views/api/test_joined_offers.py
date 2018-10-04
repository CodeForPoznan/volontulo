# -*- coding: utf-8 -*-

"""
.. module:: test_joined_offers
"""

from django.urls import reverse
from rest_framework.test import APITestCase

from apps.volontulo.factories import UserFactory
from apps.volontulo.factories import OfferFactory

ENDPOINT_URL = reverse('joined_offers')


class TestJoinedOffers(APITestCase):
    """Tests for joined-offers api."""

    def test_user_joined_no_offers(self):
        """Tests if user did not join any offer."""

        user = UserFactory()
        self.client.force_login(user=user)

        res = self.client.get(ENDPOINT_URL)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(res.data, [])

    def test_user_joined_one_offer(self):
        """Tests if user joined one offer."""

        user = UserFactory()
        self.client.force_login(user=user)

        offer = OfferFactory()
        offer.volunteers.add(user)

        res = self.client.get(ENDPOINT_URL)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(len(res.data), 1)
        self.assertEqual(offer.id, res.data[0]['id'])
        self.assertEqual(offer.title, res.data[0]['title'])

    def test_user_joined_some_offers(self):
        """Tests if user joined more than one offer."""

        user = UserFactory()
        self.client.force_login(user=user)

        OfferFactory.create_batch(2, volunteers=[user])

        # offer that user did not join
        OfferFactory(volunteers=UserFactory.create_batch(10))

        res = self.client.get(ENDPOINT_URL)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(len(res.data), 2)
