from django.test import TestCase

from geospatial.tests.helpers import create_address_data
from orders.models import Payment, PaymentMethod, CreditNetwork
from orders.serializers import PaymentSerializer
from geospatial.models import Address


# TODO: Abstract duplicated logic from TestCustomerSerializers
from orders.tests.helpers import create_payment_data
from utils.serializer_utils import enum_from_str


class TestOrdersSerializers(TestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.address_data = create_address_data()
        cls.addr = Address.objects.create(**cls.address_data)
        cls.payment_data = create_payment_data(cls.addr)
        cls.payment = Payment.objects.create(**cls.payment_data)

    @classmethod
    def tearDownClass(cls):
        Payment.objects.all().delete()
        Address.objects.all().delete()
        super().tearDownClass()

    def test_serialize_payment(self):
        """Assert that PaymentSerializer successfully serializes an instance"""
        serializer = PaymentSerializer(self.payment)
        serialized_data = serializer.data
        address_data = serialized_data.pop("billing_address")
        no_address_data = {k: v for k, v in self.payment_data.items()
                           if k != "billing_address"}

        self.assertDictEqual(serialized_data, no_address_data)
        self.assertDictEqual(address_data, self.address_data)

    def test_create_payment(self):
        """Assert the PaymentSerializer successfully creates a new instance"""
        pmnt_with_addr_data = {k: v for k, v in self.payment_data.items()}
        pmnt_with_addr_data["billing_address"] = self.address_data

        pmnt_with_enums = {k: v for k, v in self.payment_data.items()}
        method = enum_from_str(self.payment_data["method"], PaymentMethod)
        network = enum_from_str(self.payment_data["credit_network"],
                                CreditNetwork)
        pmnt_with_enums["method"] = method
        pmnt_with_enums["credit_network"] = network

        serializer = PaymentSerializer(data=pmnt_with_addr_data)
        self.assertTrue(serializer.is_valid())
        serializer.save()

        self.assertEqual(Payment.objects.filter(**pmnt_with_enums).count(), 2)
