# restaurant_details/models.py
from django.db import models

class Restaurant(models.Model):
    name = models.CharField(max_length=200)
    address = models.CharField(max_length=200)
    contact_info = models.CharField(max_length=100)
    cuisine_type = models.CharField(max_length=100)
    rating = models.FloatField()
    google_place_id = models.CharField(max_length=100, unique=True)
    latitude = models.FloatField()
    longitude = models.FloatField()
