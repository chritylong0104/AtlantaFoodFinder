from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from .models import Favorite

@login_required
def add_to_favorites(request, restaurant_id):
    favorite, created = Favorite.objects.get_or_create(
        user=request.user,
        place_id=restaurant_id,
        defaults={'name': request.POST.get('name', '')}
    )
    return redirect('restaurant_detail', place_id=restaurant_id)

@login_required
def remove_from_favorites(request, restaurant_id):
    Favorite.objects.filter(user=request.user, place_id=restaurant_id).delete()
    return redirect('restaurant_detail', place_id=restaurant_id)

@login_required
def favorites_list(request):
    favorites = Favorite.objects.filter(user=request.user).order_by('-added_on')
    return render(request, 'favorites/favorite_list.html', {'favorites': favorites})

@login_required
def toggle_favorite(request):
    if request.method == 'POST':
        place_id = request.POST.get('place_id')
        name = request.POST.get('name')
        favorite, created = Favorite.objects.get_or_create(
            user=request.user,
            place_id=place_id,
            defaults={'name': name}
        )
        if not created:
            favorite.delete()
            return JsonResponse({'status': 'removed'})
        return JsonResponse({'status': 'added'})
    return JsonResponse({'status': 'error'}, status=400)

@login_required
def favorite_restaurants(request):
    favorites = Favorite.objects.filter(user=request.user).order_by('-added_on')
    return render(request, 'favorites/favorite_list.html', {'favorites': favorites})