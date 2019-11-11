import datetime
import os
from collections import OrderedDict
from typing import List

from django.conf import settings
from django.test import TestCase

from catalog.models import Photo, Catalog
from catalog.serializers import PhotoSerializer, CatalogSerializer
from catalog.tests.helpers import create_photo_data


class TestCatalogSerializers(TestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        # Create test data
        cls.test_data = create_photo_data()

    @classmethod
    def tearDownClass(cls):
        Photo.objects.all().delete()
        Catalog.objects.all().delete()
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

    def test_serialize_catalog(self):
        """Assert Catalog model instances are serialized as expected"""
        # Get serialized data
        catalog_title = "Test Catalog"
        catalog_publish = datetime.date(year=2000, month=1, day=1)
        catalog = Catalog.objects.create(title=catalog_title,
                                         publish_date=catalog_publish)
        Photo.objects.all().update(catalog=catalog)
        serialized_data = CatalogSerializer(catalog).data

        # Compare with test data
        self.assertSetEqual({"title", "publish_date", "photos"},
                            set(serialized_data.keys()))
        self.assertEqual(serialized_data['title'], catalog_title)
        self.assertEqual(serialized_data['publish_date'],
                         catalog_publish.strftime('%Y-%m-%d'))
        self.photo_data_check(serialized_data['photos'])
