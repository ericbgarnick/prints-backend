from django.db import models
from enumfields import Enum, EnumField


class OrderStatus(Enum):
    IN_CART = "IN_CART"
    SUBMITTED = "SUBMITTED"  # customer has paid already
    SHIPPED = "SHIPPED"
    DELIVERED = "DELIVERED"
    CANCELLED = "CANCELLED"  # order was submitted and then cancelled


# TODO: Include ordered prints
class Order(models.Model):
    # SET_NULL because we may need to delete client data for
    # privacy/data control compliance but still want the order record
    customer = models.ForeignKey('customers.Customer', null=True, blank=True,
                                 on_delete=models.SET_NULL)
    shipping_address = models.ForeignKey('geospatial.Address',
                                         on_delete=models.PROTECT)
    payment = models.OneToOneField('orders.Payment', on_delete=models.PROTECT)
    order_status = EnumField(OrderStatus, max_length=16)

    def __str__(self) -> str:
        return f"Order #{self.id}: {self.customer} - {self.order_status}"

    __repr__ = __str__


class PaymentMethod(Enum):
    CREDIT = "CREDIT"
    DEBIT = "DEBIT"


class CreditNetwork(Enum):
    VISA = "VISA"
    MASTERCARD = "MASTERCARD"
    DISCOVER = "DISCOVER"
    AMEX = "AMEX"


# TODO: Include amount paid
class Payment(models.Model):
    method = EnumField(PaymentMethod, max_length=8)
    credit_network = EnumField(CreditNetwork, max_length=16, null=True)
    account_number = models.CharField(max_length=20)
    card_expiration = models.CharField(max_length=6)  # MMYYYY
    card_cvv = models.CharField(max_length=8)         # Char for leading 0's
    billing_first_name = models.CharField(max_length=64)
    billing_last_name = models.CharField(max_length=64)
    billing_address = models.ForeignKey('geospatial.Address',
                                        on_delete=models.PROTECT)

    def __str__(self) -> str:
        acct_num_anon = ('x' * (len(self.account_number) - 4)
                         + self.account_number[-4:])
        return f"{self.credit_network} ({self.method}): {acct_num_anon}"

    __repr__ = __str__
