import pycountry
import us
from django.db import models


US_STATE_ABBR = [(state.abbr, state.abbr) for state in us.states.STATES]
COUNTRY_NAMES = sorted([(c.name, c.name) for c in pycountry.countries])


class Address(models.Model):
    line1 = models.CharField(max_length=128)
    line2 = models.CharField(max_length=128, null=True, blank=True)
    city = models.CharField(max_length=64)
    state = models.CharField(choices=US_STATE_ABBR, max_length=2)
    postal_code = models.CharField(max_length=10)
    country = models.CharField(choices=COUNTRY_NAMES, max_length=128)

    def __str__(self):
        local = ('\n'.join([self.line1, self.line2])
                 if self.line2 else self.line1)
        region = f"{self.city}, {self.state} {self.postal_code}"
        return '\n'.join([local, region, self.country])

    __repr__ = __str__
