from django.test import TestCase

from geospatial.models import Address
from geospatial.serializers import AddressSerializer


class TestGeospatialSerializers(TestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.address_data = {"line1": "123 main st",
                            "line2": "apt 3", "city": "Sunnyvale",
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

    def test_create_address_new_data(self):
        """Assert the AddressSerializer successfully creates a new
        instance when address data does not match an existing address"""
        new_address = {k: v for k, v in self.address_data.items()}
        new_address["city"] = "Mountain View"
        serializer = AddressSerializer(data=new_address)
        self.assertTrue(serializer.is_valid())
        serializer.save()
        self.assertEqual(Address.objects.filter(**self.address_data).count(), 1)
        self.assertEqual(Address.objects.filter(**new_address).count(), 1)

    def test_dont_create_address_old_data(self):
        """Assert the AddressSerializer does not create a new
        instance when address data matches an existing address"""
        serializer = AddressSerializer(data=self.address_data)
        self.assertTrue(serializer.is_valid())
        serializer.save()
        self.assertEqual(Address.objects.filter(**self.address_data).count(), 1)
