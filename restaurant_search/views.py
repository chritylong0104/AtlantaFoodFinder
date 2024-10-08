from django.shortcuts import render
from django.conf import settings
import googlemaps
from geopy.distance import geodesic
from types import SimpleNamespace
import random

def get_place_photos(gmaps, place_id):
    place_details = gmaps.place(place_id=place_id, fields=['photo'])
    photos = []
    if 'photos' in place_details['result']:
        for photo in place_details['result']['photos'][:5]:  # Limit to 5 photos
            photo_reference = photo['photo_reference']
            photo_url = f"https://maps.googleapis.com/maps/api/place/photo?maxwidth=400&photo_reference={photo_reference}&key={settings.GOOGLE_MAPS_API_KEY}"
            photos.append(photo_url)
    return photos

def restaurant_search(request):
    context = {
        'GOOGLE_MAPS_API_KEY': settings.GOOGLE_MAPS_API_KEY,
        'restaurants': [],
        'search_query': '',
        'cuisine_type': '',
        'min_rating': 0,
        'max_distance': ''
    }

    if request.method in ['POST', 'GET']:
        search_query = request.POST.get('search_query', '') or request.GET.get('search_query', '')
        cuisine_type = request.POST.get('cuisine_type', '') or request.GET.get('cuisine_type', '')
        min_rating = request.POST.get('min_rating', '') or request.GET.get('min_rating', '')
        max_distance = request.POST.get('max_distance', '') or request.GET.get('max_distance', '')
        user_lat = request.POST.get('user_lat', '') or request.GET.get('user_lat', '')
        user_lng = request.POST.get('user_lng', '') or request.GET.get('user_lng', '')

        try:
            min_rating = float(min_rating) if min_rating else 0
            max_distance = float(max_distance) if max_distance else float('inf')
            user_lat = float(user_lat) if user_lat else 33.7490  # Default to Atlanta's latitude
            user_lng = float(user_lng) if user_lng else -84.3880  # Default to Atlanta's longitude
        except ValueError:
            context['error'] = "Please enter valid numbers for rating and distance."
            return render(request, 'restaurant_search/restaurant_search.html', context)

        user_location = (user_lat, user_lng)
        gmaps = googlemaps.Client(key=settings.GOOGLE_MAPS_API_KEY)

        try:
            places_result = gmaps.places(query=f'{search_query} {cuisine_type} restaurant in Atlanta')

            restaurants = []
            for place in places_result.get('results', []):
                restaurant_location = (place['geometry']['location']['lat'], place['geometry']['location']['lng'])
                distance = geodesic(user_location, restaurant_location).km
                rating = place.get('rating', 0)

                if rating >= min_rating and distance <= max_distance:
                    photo_reference = place.get('photos', [{}])[0].get('photo_reference', '')
                    image_url = f"https://maps.googleapis.com/maps/api/place/photo?maxwidth=400&photoreference={photo_reference}&key={settings.GOOGLE_MAPS_API_KEY}" if photo_reference else ''
                    restaurant = SimpleNamespace(
                        name=place['name'],
                        address=place['formatted_address'],
                        geolocation={
                            'lat': place['geometry']['location']['lat'],
                            'lng': place['geometry']['location']['lng']
                        },
                        cuisine_type=cuisine_type,
                        rating=rating,
                        distance=round(distance, 2),
                        place_id = place['place_id'],
                        image_url=image_url
                    )
                    restaurants.append(restaurant)

            restaurants.sort(key=lambda x: (-x.rating, x.distance))

            context.update({
                'restaurants': restaurants,
                'search_query': search_query,
                'cuisine_type': cuisine_type,
                'min_rating': min_rating,
                'max_distance': max_distance
            })
        except Exception as e:
            context['error'] = str(e)

    return render(request, 'restaurant_search/restaurant_search.html', context)


def restaurant_detail(request, place_id):
    gmaps = googlemaps.Client(key=settings.GOOGLE_MAPS_API_KEY)
    place_details = gmaps.place(place_id=place_id)['result']
    photo_reference = place_details.get('photos', [{}])[0].get('photo_reference', '')
    photo_url = f"https://maps.googleapis.com/maps/api/place/photo?maxwidth=1600&photoreference={photo_reference}&key={settings.GOOGLE_MAPS_API_KEY}" if photo_reference else ''

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
            'restaurant': {
            'name': place_details['name'],
            'address': place_details['formatted_address'],
            'rating': place_details['rating'],
            'latitude': place_details['geometry']['location']['lat'],
            'longitude': place_details['geometry']['location']['lng'],
            'image_url': photo_url,
            'hours': place_details.get('opening_hours', {}).get('weekday_text', []),
        },
            'place_details': place_details,
            'GOOGLE_MAPS_API_KEY': settings.GOOGLE_MAPS_API_KEY,
        }

        return render(request, 'restaurant_search/restaurant_detail.html', context)

    except Exception as e:
        context = {'error': str(e)}
        return render(request, 'restaurant_search/error.html', context)


def home(request):
    context = {
        'GOOGLE_MAPS_API_KEY': settings.GOOGLE_MAPS_API_KEY,
        'suggested_restaurants': [],
        'search_results': []
    }

    gmaps = googlemaps.Client(key=settings.GOOGLE_MAPS_API_KEY)

    # Get random restaurants for suggestions
    places_result = gmaps.places(query='restaurant in Atlanta')

    all_restaurants = []
    for place in places_result.get('results', []):
        photos = get_place_photos(gmaps, place['place_id'])
        restaurant = SimpleNamespace(
            name=place['name'],
            address=place['formatted_address'],
            geolocation={
                'lat': place['geometry']['location']['lat'],
                'lng': place['geometry']['location']['lng']
            },
            rating=place.get('rating', 0),
            photos=photos
        )
        all_restaurants.append(restaurant)

    # Randomly select up to 6 restaurants for suggestions
    num_suggestions = min(6, len(all_restaurants))
    suggested_restaurants = random.sample(all_restaurants, num_suggestions)

    for restaurant in suggested_restaurants:
        print(f"Restaurant: {restaurant.name}")
        print(f"Photos: {restaurant.photos}")
        return render(request, 'restaurant_search/homesearch.html', {'randomized_restaurants': suggested_restaurants})