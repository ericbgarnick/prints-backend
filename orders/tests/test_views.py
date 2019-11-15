from django.db import models
from django.test import TestCase
from typing import Type

from customers.models import Customer
from customers.tests.helpers import create_customer_data
from geospatial.models import Address
from geospatial.tests.helpers import create_address_data
from orders.models import Payment, Order, OrderStatus
from orders.tests.helpers import create_payment_data
from orders.views import PrintOrder


class TestOrdersViews(TestCase):
    class FakeSerializer:
        def __init__(self, instance: Type[models.Model]):
            self.instance = instance

        def save(self) -> Type[models.Model]:
            return self.instance

    def test_create_order(self):
        address = Address.objects.create(**create_address_data())
        customer = Customer.objects.create(**create_customer_data(address))
        payment = Payment.objects.create(**create_payment_data(address))

        fake_serializers = {
            "address": self.FakeSerializer(address),
            "customer": self.FakeSerializer(customer),
            "payment": self.FakeSerializer(payment)
        }

        order = PrintOrder.create_order(fake_serializers)
        self.assertIsInstance(order, Order)
        self.assertEqual(order.customer, customer)
        self.assertEqual(order.shipping_address, address)
        self.assertEqual(order.payment, payment)
        self.assertEqual(order.order_status, OrderStatus.SUBMITTED)
