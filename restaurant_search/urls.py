from django.urls import path
from . import views

urlpatterns = [
    path('restaurant-search/', views.restaurant_search, name='restaurant_search'),
    path('', views.home, name='home')
]