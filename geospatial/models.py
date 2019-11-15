import us
from django.db import models


US_STATE_ABBR = [(state.abbr, state.abbr) for state in us.states.STATES]


class Address(models.Model):
    line1 = models.CharField(max_length=128)
    line2 = models.CharField(max_length=128, null=True, blank=True)
    city = models.CharField(max_length=64)
    state = models.CharField(choices=US_STATE_ABBR, max_length=2)
    postal_code = models.CharField(max_length=10)
