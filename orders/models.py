from django.db import models
from enumfields import Enum, EnumField


class PrintSize(Enum):
    SMALL = "SMALL"
    MEDIUM = "MEDIUM"
    LARGE = "LARGE"


class PrintSizeInfo(models.Model):
    """Info about a size of prints"""
    # If no base price, the print should not be available for sale
    base_price_cents = models.PositiveIntegerField(null=True, blank=True)
    # If no ship price, the print should not be available for sale
    ship_price_cents = models.PositiveIntegerField(null=True, blank=True)
    size = EnumField(PrintSize, max_length=16)


class Print(models.Model):
    """A print of a Photo that has been purchased"""
    # size_info and photo should always exist if a print exists
    size_info = models.ForeignKey(PrintSizeInfo, on_delete=models.PROTECT)
    photo = models.ForeignKey('catalog.Photo', on_delete=models.PROTECT)
    print_number = models.PositiveIntegerField()


class OrderStatus(Enum):
    IN_CART = "IN_CART"
    SUBMITTED = "SUBMITTED"  # customer has paid already
    SHIPPED = "SHIPPED"
    DELIVERED = "DELIVERED"
    CANCELLED = "CANCELLED"  # order was submitted and then cancelled


class Order(models.Model):
    print = models.ForeignKey(Print, on_delete=models.PROTECT)
    # SET_NULL because we may need to delete client data for
    # privacy/data control compliance but still want the order record
    customer = models.ForeignKey('customers.Customer',
                                 on_delete=models.SET_NULL)
    shipping_address = models.ForeignKey('geospatial.USAddress',
                                         on_delete=models.PROTECT)
    order_status = EnumField(OrderStatus, max_length=16)
