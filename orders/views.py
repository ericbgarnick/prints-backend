from rest_framework.parsers import JSONParser
from rest_framework.response import Response
from rest_framework.serializers import ModelSerializer
from rest_framework.views import APIView
from typing import Dict, List

from customers.serializers import CustomerSerializer
from geospatial.serializers import AddressSerializer
from orders.models import Order, OrderStatus
from orders.serializers import PaymentSerializer
from photos.models import Photo
from prints.models import Print, PrintSizeInfo
from prints.serializers import PrintSerializer


class PrintOrder(APIView):
    """
    Receives orders for prints and returns a billing summary.

    Request format:
    {
        "customer": {
            "first_name": <str>,
            "last_name": <str>,
            "email": <str>,
            "phone": <str/null>,
            "address": <address**/null>
        },
        "shipping_address": <address**>,
        "prints": [
            {
                "image_id": <int>,
                "size": <SMALL/MEDIUM/LARGE>
            }
        ],
        "payment": {
            "method": <CREDIT/DEBIT>,
            "credit_network": <VISA/MASTERCARD/DISCOVER/AMEX>,
            "account_number": <str>,
            "card_expiration": <str: MMYYYY>,
            "card_cvv": <str>,
            "billing_first_name": <str>,
            "billing_last_name": <str>,
            "billing_address": <address**>
        }
    }

    Response format:
    {
        "order_num": <int>,
        "billing_summary": {
            "prints": [
                "image_title": <str>,
                "size": <SMALL/MEDIUM/LARGE>,
                "base_price_cents": <int>,
                "ship_price_cents": <int>
            ],
            "payment_method": <CREDIT/DEBIT>,
            "payment_account_end": <int>,  # last 4 digits of account number,
            "billing_first_name": <str>,
            "billing_last_name": <str>,
            "billing_address": <address**>,
            "shipping_address": <address**>
        }
    }

    ** address: {
        "line1": <str>,
        "line2": <str/null>,
        "city": <str>,
        "state": <str>,
        "postal_code": <str>,
    }

    """
    def get(self, request):
        """Avoid error on DRF default page"""
        return Response()

    def post(self, request):
        data = JSONParser().parse(request)
        customer_data = data.get("customer")
        shipping_address_data = data.get("shipping_address")
        prints_data = data.get("prints")
        payment_data = data.get("payment")

        serializers = {
            "customer": CustomerSerializer(data=customer_data),
            "address": AddressSerializer(data=shipping_address_data),
            "prints": PrintSerializer(data=prints_data, many=True),
            "payment": PaymentSerializer(data=payment_data)
        }

        good_data = True
        ret_data = {}

        for s in serializers.values():
            if not s.is_valid():
                good_data = False

        if good_data:
            order = self.create_order(serializers)
            self.create_prints_for_order(serializers, order)

            billing_summary = {}
            self.add_payment_info(billing_summary, payment_data)
            self.add_shipping_info(billing_summary, shipping_address_data)
            self.add_prints_info(billing_summary, prints_data)

            ret_data["order_num"] = order.id
            ret_data["billing_summary"] = billing_summary

        response_status = 201 if good_data else 422

        return Response(data=ret_data, status=response_status)

    @staticmethod
    def create_order(serializers: Dict[str, ModelSerializer]) -> Order:
        """Create order from chaos (and customer, address, payment instances)"""
        customer = serializers["customer"].save()
        address = serializers["address"].save()
        payment = serializers["payment"].save()
        return Order.objects.create(
            customer=customer, shipping_address=address,
            payment=payment, order_status=OrderStatus.SUBMITTED)

    @staticmethod
    def create_prints_for_order(serializers: Dict[str, ModelSerializer],
                                order: Order):
        """Create prints with FK reference to order argument"""
        prints = serializers["prints"].save()
        print_ids = [p.id for p in prints]
        Print.objects.filter(id__in=print_ids).update(order=order)

    @staticmethod
    def add_payment_info(billing_summary: Dict, payment_data: Dict):
        """Update billing_summary with payment_data info"""
        billing_summary["payment_method"] = payment_data["method"]
        acct_num = payment_data["account_number"]
        billing_summary["payment_account_end"] = acct_num[-4:]
        billing_summary["billing_first_name"] = payment_data["billing_first_name"]
        billing_summary["billing_last_name"] = payment_data["billing_last_name"]
        billing_summary["billing_address"] = payment_data["billing_address"]

    @staticmethod
    def add_shipping_info(billing_summary: Dict, shipping_data: Dict):
        """Update billing_summary with shipping_data info"""
        billing_summary["shipping_address"] = shipping_data

    @staticmethod
    def add_prints_info(billing_summary: Dict, prints_data: List[Dict]):
        """Update billing_summary with prints_data info"""
        prints_summary = []
        print_size_info = PrintSizeInfo.objects.all().values_list(
            "size", "base_price_cents", "ship_price_cents")
        size_info_cache = {s.value.upper(): {"base_price": bp, "ship_price": sp}
                           for s, bp, sp in print_size_info}
        for print_data in prints_data:
            PrintOrder._add_single_print(print_data,
                                         size_info_cache,
                                         prints_summary)
        billing_summary["prints"] = prints_summary

    @staticmethod
    def _add_single_print(print_data: Dict, size_info_cache: Dict,
                          prints_summary: List[Dict]):
        """Add dict for print_data to prints_summary."""
        image_title = Photo.objects.get(image_id=print_data["image_id"]).title
        size = print_data["size"]
        base_price = size_info_cache[size]["base_price"]
        ship_price = size_info_cache[size]["ship_price"]
        prints_summary.append({
            "image_title": image_title,
            "size": size,
            "base_price_cents": base_price,
            "ship_price_cents": ship_price
        })
