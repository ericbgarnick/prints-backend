from django.db import models


class Customer(models.Model):
    first_name = models.CharField(max_length=64)
    last_name = models.CharField(max_length=64)
    # Non-nullable: we need to be able to contact customers about their orders
    email = models.CharField(max_length=128)
    # 10 digits, optionally prepended with '1' or '+1'
    phone = models.CharField(max_length=12, null=True, blank=True)
    # For promotional material and other correspondence,
    # may differ from shipping address
    address = models.ForeignKey('geospatial.Address',
                                on_delete=models.PROTECT)

    def __str__(self) -> str:
        return f"{self.first_name} {self.last_name} ({self.email})"

    __repr__ = __str__
