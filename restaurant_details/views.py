# restaurant_details/views.py
from django.shortcuts import render, redirect
from .models import Restaurant
import googlemaps
from django.conf import settings
from django.shortcuts import render, get_object_or_404
from restaurant_search.models import Restaurant  # Adjust this import based on where your Restaurant model is defined
from types import SimpleNamespace
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

def search_restaurants(request):
    if request.method == 'POST':
        query = request.POST.get('query')
        gmaps = googlemaps.Client(key=settings.GOOGLE_MAPS_API_KEY)

        # Search for restaurants
        places_result = gmaps.places(query=query, type='restaurant')

        for place in places_result['results']:
            Restaurant.objects.update_or_create(
                google_place_id=place['place_id'],
                defaults={
                    'name': place['name'],
                    'address': place['formatted_address'],
                    'latitude': place['geometry']['location']['lat'],
                    'longitude': place['geometry']['location']['lng'],
                    'rating': place.get('rating', 0),
                }
            )

        return redirect('restaurant_list')

    return render(request, 'restaurant_details/search.html')

# restaurant_details/views.py
def restaurant_list(request):
    restaurants = Restaurant.objects.all()
    return render(request, 'restaurant_details/restaurant_list.html', {'restaurants': restaurants})


# restaurant_details/views.py
from django.shortcuts import get_object_or_404


def restaurant_detail(request, place_id):
    gmaps = googlemaps.Client(key=settings.GOOGLE_MAPS_API_KEY)

    try:
        place_result = gmaps.place(place_id=place_id)
        place_details = place_result['result']

        restaurant = SimpleNamespace(
            name=place_details['name'],
            address=place_details['formatted_address'],
            geolocation={
                'lat': place_details['geometry']['location']['lat'],
                'lng': place_details['geometry']['location']['lng']
            },
            phone_number=place_details.get('formatted_phone_number', 'N/A'),
            website=place_details.get('website', 'N/A'),
            rating=place_details.get('rating', 'N/A'),
            reviews=place_details.get('reviews', [])
        )

        context = {
            'restaurant': restaurant,
            'GOOGLE_MAPS_API_KEY': settings.GOOGLE_MAPS_API_KEY
        }

        return render(request, 'restaurant_search/restaurant_detail.html', context)

    except Exception as e:
        context = {'error': str(e)}
        return render(request, 'restaurant_search/error.html', context)