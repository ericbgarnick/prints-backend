import locale

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

    def __str__(self) -> str:
        base_price_dollars = self.base_price_cents / 100
        ship_price_dollars = self.ship_price_cents / 100
        return (f"{self.size} @ "
                f"${base_price_dollars:.2f} base + "
                f"${ship_price_dollars:.2f} shipping")

    __repr__ = __str__


class Print(models.Model):
    """A purchased print of a Photo"""
    order = models.ForeignKey('orders.Order', null=True, on_delete=models.PROTECT)
    # size_info and photo should always exist if a print exists
    size_info = models.ForeignKey(PrintSizeInfo, on_delete=models.PROTECT)
    photo = models.ForeignKey('photos.Photo', on_delete=models.PROTECT)
    print_number = models.PositiveIntegerField()

    def __str__(self) -> str:
        return (f"Order num {self.order.id}: "
                f"\"{self.photo.title}\" "
                f"({self.print_number}/{self.photo.max_prints})"
                f" - size: {self.size_info.size.value.lower()} ")

    __repr__ = __str__
