"""
.. module:: test_is_offer_joined_filter
"""

from rest_framework import status
from rest_framework.test import APITestCase

from apps.volontulo.factories import UserFactory
from apps.volontulo.factories import OfferFactory


class IsOfferJoinedFilterTestCase(APITestCase):

    """Tests for joined=? filter."""

    def setUp(self):
        super().setUp()
        user = UserFactory()
        self.client.force_login(user)
        OfferFactory.create_batch(
            67,
            offer_status='published',
            finished_at=None,
            recruitment_end_date=None,
            volunteers=UserFactory.create_batch(20)
        )
        OfferFactory.create_batch(
            73,
            offer_status='published',
            finished_at=None,
            recruitment_end_date=None,
            volunteers=UserFactory.create_batch(20) + [user]
        )

    def test_all_offers(self):
        response = self.client.get('/api/offers/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 67 + 73)

    def test_joined_offers(self):
        response = self.client.get('/api/offers/?joined=true')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 73)

    def test_unjoined_offers(self):
        response = self.client.get('/api/offers/?joined=false')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 67)

    def test_unaccepted_values(self):
        response = self.client.get('/api/offers/?joined=True')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 67 + 73)

        response = self.client.get('/api/offers/?joined=False')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 67 + 73)

        response = self.client.get('/api/offers/?joined=')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 67 + 73)
