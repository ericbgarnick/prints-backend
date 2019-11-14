from django.db import models


class TestModel(models.Model):
    """A model for unit testing so that util tests do not rely
     on schema for models in other apps."""
    numeric_str = models.CharField(max_length=5)
