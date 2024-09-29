# models.py
from django.db import models
from django_google_maps import fields as map_fields


class Restaurant(models.Model):
    name = models.CharField(max_length=100)
    address = models.CharField(max_length=200)
    geolocation = models.CharField(max_length=50)
    cuisine_type = models.CharField(max_length=50)
    rating = models.FloatField()

    @property
    def distance(self):
        return getattr(self, '_distance', None)

    @distance.setter
    def distance(self, value):
        self._distance = value