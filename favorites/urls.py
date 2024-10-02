from django.urls import path
from . import views

urlpatterns = [
    path('toggle/', views.toggle_favorite, name='toggle_favorite'),
    path('', views.favorites_list, name='favorites_list'),
]