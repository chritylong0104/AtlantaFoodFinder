from django.db import models
from django_google_maps import fields as map_fields

class Restaurant(models.Model):
    name = models.CharField(max_length=100)
    address = map_fields.AddressField(max_length=200)
    geolocation = map_fields.GeoLocationField(max_length=100)
    # Add any other fields you need, such as ratings, cuisine type, etc.

    def __str__(self):
        return self.name