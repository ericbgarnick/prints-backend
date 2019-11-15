from django.test import TestCase

from customers.models import Customer
from customers.serializers import CustomerSerializer
from customers.tests.helpers import create_customer_data
from geospatial.models import Address
from geospatial.tests.helpers import create_address_data


class TestCustomerSerializers(TestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.address_data = create_address_data()
        cls.usa = Address.objects.create(**cls.address_data)
        cls.customer_data = create_customer_data(cls.usa)
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
