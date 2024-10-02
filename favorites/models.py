from django.db import models
from django.contrib.auth.models import User
from restaurant_search.models import Restaurant  # Adjust this import based on your project structure

class Favorite(models.Model):
    name = models.CharField(max_length=36, null=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    restaurant = models.ForeignKey(Restaurant, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    is_favourite = models.ManyToManyField(User, related_name='favourite', blank=True)

    class Meta:
        unique_together = ('user', 'restaurant')

    def __str__(self):
        return f"{self.user.username} - {self.restaurant.name}"