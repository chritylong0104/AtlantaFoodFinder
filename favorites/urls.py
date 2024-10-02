from django.urls import path
from . import views

app_name = 'favorites'
urlpatterns = [
    path('toggle-favorite/<int:restaurant_id>/', views.toggle_favorite, name='toggle_favorite'),
    path('', views.favorites_list, name='favorites_list'),
]