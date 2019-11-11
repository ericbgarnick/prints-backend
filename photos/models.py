from django.db import models


class Photo(models.Model):
    """A photo of which prints may have been Prints."""
    image_id = models.PositiveIntegerField(primary_key=True)
    image_location = models.ImageField(upload_to='photos')
    title = models.CharField(max_length=256)
    shot_date = models.DateField()
    max_prints = models.PositiveIntegerField()
