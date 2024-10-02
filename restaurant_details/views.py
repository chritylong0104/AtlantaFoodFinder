from django.shortcuts import render, redirect
from django.conf import settings
import googlemaps
from django.http import Http404
from favorites.models import Favorite


def home_view(request):
    return render(request, 'home.html')

def restaurant_search(request):
    if request.method == 'POST':
        query = request.POST.get('query')
        gmaps = googlemaps.Client(key=settings.GOOGLE_MAPS_API_KEY)

        # Search for restaurants
        places_result = gmaps.places(query=query, type='restaurant')

        restaurants = []
        for place in places_result['results']:
            restaurants.append({
                'name': place['name'],
                'address': place['formatted_address'],
                'place_id': place['place_id'],
                'rating': place.get('rating', 'N/A'),
            })

        context = {
            'restaurants': restaurants,
            'query': query,
        }
        return render(request, 'restaurant_details/search_results.html', context)

    return render(request, 'restaurant_details/search.html')

def restaurant_detail(request, place_id):
    gmaps = googlemaps.Client(key=settings.GOOGLE_MAPS_API_KEY)

    try:
        place_result = gmaps.place(place_id=place_id, fields=[
            'name', 'formatted_address', 'geometry', 'formatted_phone_number',
            'website', 'rating', 'reviews', 'opening_hours', 'photos'
        ])
        place_details = place_result['result']

        restaurant = {
            'name': place_details['name'],
            'address': place_details['formatted_address'],
            'latitude': place_details['geometry']['location']['lat'],
            'longitude': place_details['geometry']['location']['lng'],
            'phone_number': place_details.get('formatted_phone_number', 'N/A'),
            'website': place_details.get('website', 'N/A'),
            'rating': place_details.get('rating', 'N/A'),
            'reviews': place_details.get('reviews', []),
            'hours': place_details.get('opening_hours', {}).get('weekday_text', []),
            'image_url': place_details.get('photos', [{}])[0].get('photo_reference', '')
        }

        context = {
            'restaurant': restaurant,
            'GOOGLE_MAPS_API_KEY': settings.GOOGLE_MAPS_API_KEY
        }

        return render(request, 'restaurant_details/restaurant_detail.html', context)

    except Exception as e:
        raise Http404(f"Restaurant with place_id {place_id} not found")
    is_favorite = False
    if request.user.is_authenticated:
        is_favorite = Favorite.objects.filter(user=request.user, place_id=place_id).exists()

    context = {
        'place': place_details,
        'GOOGLE_MAPS_API_KEY': api_key,
        'is_favorite': is_favorite,
    }
    return render(request, 'restaurant_search/restaurant_detail.html', context)

def restaurant_list(request):
    # This function is left as a placeholder.
    # You might want to implement this if you need a list view of restaurants.
    return render(request, 'restaurant_details/restaurant_list.html')

# Commented out as it's not currently used
# def search_restaurants(request):
#     if request.method == 'POST':
#         query = request.POST.get('query')
#         gmaps = googlemaps.Client(key=settings.GOOGLE_MAPS_API_KEY)
#
#         # Search for restaurants
#         places_result = gmaps.places(query=query, type='restaurant')
#
#         for place in places_result['results']:
#             Restaurant.objects.update_or_create(
#                 google_place_id=place['place_id'],
#                 defaults={
#                     'name': place['name'],
#                     'address': place['formatted_address'],
#                     'latitude': place['geometry']['location']['lat'],
#                     'longitude': place['geometry']['location']['lng'],
#                     'rating': place.get('rating', 0),
#                 }
#             )
#
#         return redirect('restaurant_list')
#
#     return render(request, 'restaurant_details/search.html')