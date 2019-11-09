import datetime

from django.db import models


class Catalog(models.Model):
    """A catalogs of Photos for which Prints are available for purchase"""
    title = models.CharField(max_length=256)
    publish_date = models.DateField(default=datetime.date.today)


class Photo(models.Model):
    """A photo that may be part of a Catalog and
    may have Prints available for purchase."""
    image = models.ImageField()
    title = models.CharField(max_length=256)
    shot_date = models.DateField()
    max_prints = models.PositiveIntegerField()
    catalog = models.ForeignKey(Catalog, on_delete=models.SET_NULL,
                                null=True, blank=True)
