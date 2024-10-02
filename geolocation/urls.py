from django.urls import path
from . import views

urlpatterns = [
    path('', views.home_view, name='home'),
    path('map/', views.map_view, name='map_view'),
    path('restaurant/<str:place_id>/', views.restaurant_detail, name='restaurant_detail'),
path('favorites/', views.favorites_list, name='favorites_list'),
path('toggle-favorite/', views.toggle_favorite, name='toggle_favorite'),
]