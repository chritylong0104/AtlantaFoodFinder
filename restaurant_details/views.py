from django.shortcuts import render, get_object_or_404
from restaurant_search.models import Restaurant  # Adjust this import based on where your Restaurant model is defined
from favorites.models import Favorite

# #this is to check if restaurant is favorited; commented for now
# def restaurant_detail(request, restaurant_id):
#     restaurant = get_object_or_404(Restaurant, id=restaurant_id)
#     is_favorite = False
#     if request.user.is_authenticated:
#         is_favorite = Favorite.objects.filter(user=request.user, restaurant=restaurant).exists()
#     return render(request, 'restaurant_details/restaurant_detail.html', {
#         'restaurant': restaurant,
#         'is_favorite': is_favorite
#     })