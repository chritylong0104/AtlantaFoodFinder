from django.db import models
from django_google_maps import fields as map_fields

class Restaurant(models.Model):
    name = models.CharField(max_length=100)
    address = map_fields.AddressField(max_length=200)
    geolocation = map_fields.GeoLocationField(max_length=100)
    cuisine = models.CharField(max_length=100, default='Unknown')
    latitude = models.FloatField(null=True, blank=True)
    longitude = models.FloatField(null=True, blank=True)

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        if self.geolocation:
            lat, lng = self.geolocation.split(',')
            self.latitude = float(lat.strip())
            self.longitude = float(lng.strip())
        super().save(*args, **kwargs)