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
    @property
    def size_abbr(self) -> str:
        return self.size.value[0]


class Print(models.Model):
    """A print of a Photo that has been purchased"""
    # size_info and photo should always exist if a print exists
    size_info = models.ForeignKey(PrintSizeInfo, on_delete=models.PROTECT)
    photo = models.ForeignKey('catalogs.Photo', on_delete=models.PROTECT)
    print_number = models.PositiveIntegerField()