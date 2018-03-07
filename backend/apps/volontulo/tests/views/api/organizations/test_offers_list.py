"""
.. module:: test_offers_list
"""

from django.test import TestCase

from apps.volontulo.factories import OfferFactory
from apps.volontulo.tests import common


class TestOrganizationOffers(TestCase):

    """ Tests for organization's offers API """

    def setUp(self):
        """ Set up for each test """
        self.offer = OfferFactory.create()
        self.offer.publish()

    def test_404_if_org_does_not_exist(self):
        """ Test for getting an organization """
        res = self.client.get('/api/organizations/666999/offers/')
        self.assertEqual(res.status_code, 404)

    def test_405_if_method_not_alowed(self):
        """ Test for using wrong method """
        res = self.client.post(
            '/api/organizations/{}/offers/'
            .format(self.offer.organization.id))
        self.assertEqual(res.status_code, 405)

    def test_200(self):
        """ Test for gettin offers list """
        res = self.client.get(
            '/api/organizations/{}/offers/'
            .format(self.offer.organization.id))
        self.assertEqual(res.status_code, 200)
        for offer in res.data:
            common.test_offer_list_fields(self, offer)
