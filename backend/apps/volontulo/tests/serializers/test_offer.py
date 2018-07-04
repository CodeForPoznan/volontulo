"""
.. module:: test_offer
"""

from urllib.parse import urlparse

from django.contrib.auth.models import AnonymousUser
from django.test import TestCase
from django.test.client import RequestFactory

from apps.volontulo.factories import OfferFactory
from apps.volontulo.serializers import OfferSerializer


class TestOfferSerializer(TestCase):

    """Test for offers serializer."""

    def test_image(self):
        """Test image field."""
        offer = OfferFactory()
        request = RequestFactory().get('/')
        request.user = AnonymousUser()
        self.assertEqual(urlparse(OfferSerializer(
            offer,
            context={'request': request},
        ).data['image']).path, offer.image.url)

    def test_slug(self):
        """Test slug method."""
        offer = OfferFactory(title='Offer Title 123')
        self.assertEqual(OfferSerializer().get_slug(offer), 'offer-title-123')
