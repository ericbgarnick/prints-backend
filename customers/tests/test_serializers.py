from django.test import TestCase

from customers.models import Customer
from customers.serializers import CustomerSerializer
from geospatial.models import Address


class TestCustomerSerializers(TestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.address_data = {"line1": "123 main st",
                            "line2": "apt 3", "city": "Sunnyvale",
                            "state": "CA", "postal_code": "94085",
                            "country": "United States"}
        cls.usa = Address.objects.create(**cls.address_data)
        cls.customer_data = {"first_name": "Test",
                             "last_name": "McTest",
                             "email": "test@test.com",
                             "phone": "+13334445555",
                             "address": cls.usa}
        cls.customer = Customer.objects.create(**cls.customer_data)

    @classmethod
    def tearDownClass(cls):
        Customer.objects.all().delete()
        Address.objects.all().delete()
        super().tearDownClass()

    def test_serialize_customer(self):
        """Assert that CustomerSerializer successfully serializes an instance"""
        serializer = CustomerSerializer(self.customer)
        serialized_data = serializer.data
        address_data = serialized_data.pop("address")
        no_address_data = {k: v for k, v in self.customer_data.items()
                           if k != "address"}

        self.assertDictEqual(serialized_data, no_address_data)
        self.assertDictEqual(address_data, self.address_data)

    def test_create_customer(self):
        """Assert the CustomerSerializer successfully creates a new instance"""
        cust_with_addr_data = {k: v for k, v in self.customer_data.items()}
        cust_with_addr_data["address"] = self.address_data

        serializer = CustomerSerializer(data=cust_with_addr_data)
        self.assertTrue(serializer.is_valid())
        serializer.save()
        self.assertEqual(Customer.objects.filter(**self.customer_data).count(), 2)
