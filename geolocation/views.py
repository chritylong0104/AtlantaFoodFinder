from django.shortcuts import render
from django.conf import settings
from .models import Restaurant
from django.db.models import Q

def map_view(request):
    query = request.GET.get('query', '')

    if query:
        restaurants = Restaurant.objects.filter(
            Q(name__icontains=query) |
            Q(address__icontains=query) |
            Q(cuisine__icontains=query)
        )
    else:
        restaurants = Restaurant.objects.all()

    context = {
        'restaurants': restaurants,
        'GOOGLE_MAPS_API_KEY': settings.GOOGLE_MAPS_API_KEY,
        'query': query,
    }
    return render(request, 'geolocation/map.html', context)

def home_view(request):
    return render(request, 'geolocation/home.html')
