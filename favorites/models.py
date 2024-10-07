from django.db import models
from django.contrib.auth.models import User

class Favorite(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='favorites')
    place_id = models.CharField(max_length=255, default='default_place_id')
    name = models.CharField(max_length=255, default='Unnamed Favorite')
    address = models.TextField(blank=True, null=True)
    image_url = models.URLField(max_length=1000, blank=True, null=True)
    rating = models.FloatField(null=True, blank=True)
    added_on = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('user', 'place_id')

    def __str__(self):
        return f"{self.user.username}'s favorites: {self.name}"