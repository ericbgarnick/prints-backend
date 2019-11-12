from django.db import models
from enumfields import Enum, EnumField


class OrderStatus(Enum):
    IN_CART = "IN_CART"
    SUBMITTED = "SUBMITTED"  # customer has paid already
    SHIPPED = "SHIPPED"
    DELIVERED = "DELIVERED"
    CANCELLED = "CANCELLED"  # order was submitted and then cancelled


class Order(models.Model):
    # SET_NULL because we may need to delete client data for
    # privacy/data control compliance but still want the order record
    customer = models.ForeignKey('customers.Customer', null=True, blank=True,
                                 on_delete=models.SET_NULL)
    shipping_address = models.ForeignKey('geospatial.USAddress',
                                         on_delete=models.PROTECT)
    order_status = EnumField(OrderStatus, max_length=16)
