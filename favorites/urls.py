from django.urls import path
from . import views

urlpatterns = [
    path('add/<int:restaurant_id>/', views.add_to_favorites, name='add_to_favorites'),
    path('remove/<int:restaurant_id>/', views.remove_from_favorites, name='remove_from_favorites'),
    path('list/', views.favorites_list, name='favorites_list') ]