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
    """Receives orders for prints and returns a billing summary"""
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

        response_status = 200 if good_data else 422

        return Response(data=ret_data, status=response_status)

    @staticmethod
    def create_order(serializers: Dict[str, ModelSerializer]) -> Order:
        customer = serializers["customer"].save()
        address = serializers["address"].save()
        payment = serializers["payment"].save()
        return Order.objects.create(
            customer=customer, shipping_address=address,
            payment=payment, order_status=OrderStatus.SUBMITTED)

    @staticmethod
    def create_prints_for_order(serializers: Dict[str, ModelSerializer],
                                order: Order):
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
        billing_summary["prints"] = prints_summary
