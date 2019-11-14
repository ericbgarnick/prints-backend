from rest_framework.parsers import JSONParser
from rest_framework.response import Response
from rest_framework.views import APIView

from customers.serializers import CustomerSerializer
from geospatial.serializers import AddressSerializer
from orders.models import Order, OrderStatus
from orders.serializers import PaymentSerializer
from prints.models import Print
from prints.serializers import PrintSerializer


class PrintOrder(APIView):
    """Receives orders for prints and returns a billing summary"""
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
        for s in serializers.values():
            if not s.is_valid():
                good_data = False
        if good_data:
            customer = serializers["customer"].save()
            address = serializers["address"].save()
            prints = serializers["prints"].save()
            payment = serializers["payment"].save()
            order = Order.objects.create(
                customer=customer, shipping_address=address,
                payment=payment, order_status=OrderStatus.SUBMITTED)
            print_ids = [p.id for p in prints]
            Print.objects.filter(id__in=print_ids).update(order=order)
        response_status = 200 if good_data else 422
        return Response(status=response_status)
