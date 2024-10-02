from django.urls import path
from . import views

urlpatterns = [
    path('add/<str:restaurant_id>/', views.add_to_favorites, name='add_to_favorites'),
    path('remove/<str:restaurant_id>/', views.remove_from_favorites, name='remove_from_favorites'),
    path('list/', views.favorites_list, name='favorites_list'),
    path('toggle/', views.toggle_favorite, name='toggle_favorite'),
    path('my-favorites/', views.favorite_restaurants, name='favorite_restaurants'),
]