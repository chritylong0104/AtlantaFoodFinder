from django.urls import path
from . import views

urlpatterns = [
    path('restaurant-search/', views.restaurant_search, name='restaurant_search'),
    path('restaurant-detail/<str:place_id>/', views.restaurant_detail, name='restaurant_detail'),
    path('', views.home, name='home')
]