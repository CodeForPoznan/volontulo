# -*- coding: utf-8 -*-

"""
.. module:: test_offer
"""

from urllib.parse import urlparse

from django.core.files.uploadedfile import SimpleUploadedFile
from django.test import TestCase
from django.test.client import RequestFactory

from apps.volontulo.models import Offer
from apps.volontulo.models import OfferImage
from apps.volontulo.models import Organization
from apps.volontulo.serializers import OfferSerializer


class TestOfferSerializer(TestCase):

    """Test for offers's serializer."""

    def test_image(self):
        """Test image method."""
        organization = Organization()
        organization.save()
        offer = Offer(title='Offer Title 123', organization=organization)
        offer.save()
        image = OfferImage(offer=offer, path=SimpleUploadedFile(
            name='test_image.jpg',
            content=b'test_content',
        ))
        image.save()
        context = {
            'request': RequestFactory().get('/')
        }

        self.assertEqual(
            urlparse(OfferSerializer(context=context).get_image(offer)).path,
            image.path.url,
        )

    def test_slug(self):
        """Test slug method."""
        offer = Offer(title='Offer Title 123')
        self.assertEqual(OfferSerializer().get_slug(offer), 'offer-title-123')
