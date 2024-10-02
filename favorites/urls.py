from django.urls import path
from . import views

urlpatterns = [
    # ... other URL patterns ...
    path('toggle-favorite/', views.toggle_favorite, name='toggle_favorite'),
    path('favorites/', views.favorites_list, name='favorites_list'),
]