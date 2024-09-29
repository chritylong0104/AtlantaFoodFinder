from django.urls import path
from . import views

urlpatterns = [
    path('restaurant-search/', views.restaurant_search, name='restaurant_search'),
]