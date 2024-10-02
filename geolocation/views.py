from django.shortcuts import render
from django.conf import settings
from .models import Restaurant
from django.db.models import Q
import requests


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
    context = {
        'GOOGLE_MAPS_API_KEY': settings.GOOGLE_MAPS_API_KEY,
    }
    return render(request, 'geolocation/home.html', context)


def restaurant_detail(request, place_id):
    api_key = settings.GOOGLE_MAPS_API_KEY
    url = f"https://maps.googleapis.com/maps/api/place/details/json?place_id={place_id}&fields=name,formatted_address,rating,reviews,photos,opening_hours,formatted_phone_number,geometry&key={api_key}"

    response = requests.get(url)
    place_details = response.json()['result']

    context = {
        'place': place_details,
        'GOOGLE_MAPS_API_KEY': api_key,
    }
    return render(request, 'restaurant_search/restaurant_detail.html', context)