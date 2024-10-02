from django.db import models
from django.contrib.auth.models import User

class Favorite(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='favorites')
    place_id = models.CharField(max_length=255, default='default_place_id')
    name = models.CharField(max_length=255, default='Unnamed Favorite')
    added_on = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('user', 'place_id')

    def __str__(self):
        return f"{self.user.username} - {self.name}"