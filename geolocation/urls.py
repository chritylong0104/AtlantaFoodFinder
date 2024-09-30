from django.urls import path
from . import views

urlpatterns = [
    path('', views.home_view, name='home'),
    path('map/', views.map_view, name='map_view'),
]