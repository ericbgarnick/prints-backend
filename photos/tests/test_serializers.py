import os
from collections import OrderedDict
from typing import List

from django.conf import settings
from django.test import TestCase

from photos.models import Photo
from photos.serializers import PhotoSerializer
from photos.tests.helpers import create_photo_data


class TestCatalogSerializers(TestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        # Create test data
        cls.test_data = create_photo_data()

    @classmethod
    def tearDownClass(cls):
        Photo.objects.all().delete()
        super().tearDownClass()

    def photo_data_check(self, received_data: List[OrderedDict]):
        """Assert that received_data matches self.test_data"""
        self.assertEqual(len(received_data), len(self.test_data))
        for i, ser_d in enumerate(received_data):
            # Don't edit original test data
            test_d = {k: v for k, v in self.test_data[i].items()}
            test_d['shot_date'] = test_d['shot_date'].strftime('%Y-%m-%d')
            test_d['image_location'] = os.path.join(settings.MEDIA_URL,
                                                    test_d['image_location'])
            self.assertDictEqual(dict(ser_d), test_d)

    def test_serialize_photo(self):
        """Assert Photo model instances are serialized as expected"""
        # Get serialized data
        all_photos = Photo.objects.all().order_by('-shot_date')
        serialized_data = PhotoSerializer(all_photos, many=True).data

        # Compare with test data
        self.photo_data_check(serialized_data)
