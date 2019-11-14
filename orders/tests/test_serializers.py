from django.test import TestCase

from orders.models import Payment, PaymentMethod, CreditNetwork
from orders.serializers import PaymentSerializer
from geospatial.models import Address


# TODO: Abstract duplicated logic from TestCustomerSerializers
from utils.serializer_utils import enum_from_str


class TestOrdersSerializers(TestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.address_data = {"street": "123 main st",
                            "unit": "apt 3", "city": "Sunnyvale",
                            "state": "CA", "postal_code": "94085"}
        cls.addr = Address.objects.create(**cls.address_data)
        cls.payment_data = {'method': "Credit", 'credit_network': 'Visa',
                            'account_number': '0123456789012345',
                            'card_expiration': '012020',
                            'card_cvv': '1234', 'billing_name': 'Account Holder',
                            'billing_address': cls.addr}
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
