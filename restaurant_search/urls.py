from django.urls import path
from . import views

urlpatterns = [
    path('', views.restaurant_search, name='restaurant_search'),
    path('detail/<str:place_id>/', views.restaurant_detail, name='restaurant_detail'),
    path('', views.home, name='home')
]
