from django.shortcuts import render
from django.http import JsonResponse
from django.views.decorators.http import require_POST
from django.contrib.auth.decorators import login_required
from .models import Favorite

@login_required
@require_POST
def toggle_favorite(request):
    place_id = request.POST.get('place_id')
    name = request.POST.get('name')
    image_url = request.POST.get('image_url')
    rating = request.POST.get('rating')
    address = request.POST.get('address')
    favorite, created = Favorite.objects.get_or_create(
        user=request.user,
        place_id=place_id,
        defaults={'name': name,
                  'image_url': image_url,
                  'rating': rating,
                  'address': address
                  }
    )
    if not created:
        favorite.delete()
        return JsonResponse({'status': 'removed'})
    return JsonResponse({'status': 'added'})
@login_required
def favorites_list(request):
    favorites = Favorite.objects.filter(user=request.user).order_by('-added_on')
    return render(request, 'favorites/favorites_list.html', {'favorites': favorites})