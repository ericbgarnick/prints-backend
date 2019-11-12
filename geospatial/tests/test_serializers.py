from django.test import TestCase

from geospatial.models import Address
from geospatial.serializers import AddressSerializer


class TestGeospatialSerializers(TestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.address_data = {"street": "123 main st",
                            "unit": "apt 3", "city": "Sunnyvale",
                            "state": "CA", "postal_code": "94085"}
        cls.usa = Address.objects.create(**cls.address_data)

    @classmethod
    def tearDownClass(cls):
        Address.objects.all().delete()
        super().tearDownClass()

    def test_serialize_address(self):
        """Assert that AddressSerializer successfully serializes an instance"""
        serializer = AddressSerializer(self.usa)
        self.assertDictEqual(serializer.data, self.address_data)

    def test_create_address(self):
        """Assert the AddressSerializer successfully creates a new instance"""
        serializer = AddressSerializer(data=self.address_data)
        self.assertTrue(serializer.is_valid())
        serializer.save()
        self.assertEqual(Address.objects.filter(**self.address_data).count(), 2)



