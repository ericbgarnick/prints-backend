from django.test import TestCase

from geospatial.models import USAddress
from geospatial.serializers import USAddressSerializer


class TestGeospatialSerializers(TestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.address_data = {"street": "123 main st",
                            "unit": "apt 3", "city": "Sunnyvale",
                            "state": "CA", "postal_code": "94085"}
        cls.usa = USAddress.objects.create(**cls.address_data)

    @classmethod
    def tearDownClass(cls):
        USAddress.objects.all().delete()
        super().tearDownClass()

    def test_serialize_us_address(self):
        """Assert that USAddressSerializer successfully serializes an instance"""
        serializer = USAddressSerializer(self.usa)
        self.assertDictEqual(serializer.data, self.address_data)

    def test_create_us_address(self):
        """Assert the USAddressSerializer successfully creates a new instance"""
        serializer = USAddressSerializer(data=self.address_data)
        self.assertTrue(serializer.is_valid())
        serializer.save()
        self.assertEqual(USAddress.objects.filter(**self.address_data).count(), 2)



