from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import Favorite
from restaurant_search.models import Restaurant  # Adjust import as needed

@login_required
def add_to_favorites(request, restaurant_id):
    restaurant = get_object_or_404(Restaurant, id=restaurant_id)
    Favorite.objects.get_or_create(user=request.user, restaurant=restaurant)
    return redirect('restaurant_detail', restaurant_id=restaurant_id)

@login_required
def remove_from_favorites(request, restaurant_id):
    Favorite.objects.filter(user=request.user, restaurant_id=restaurant_id).delete()
    return redirect('favorites_list')

@login_required
def favorites_list(request):
    favorites = Favorite.objects.filter(user=request.user)
    return render(request, 'favorites/favorites_list.html', {'favorites': favorites})