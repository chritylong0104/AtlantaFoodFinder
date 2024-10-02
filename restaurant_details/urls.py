from django.urls import path
from . import views

urlpatterns = [
    path('', views.home_view, name='home'),
    path('restaurant-search/', views.restaurant_search, name='restaurant_search'),
    path('restaurant/<str:place_id>/', views.restaurant_detail, name='restaurant_detail'),
]