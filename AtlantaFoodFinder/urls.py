from django.contrib import admin
from django.urls import path, include
from restaurant_search import views as restaurant_views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', restaurant_views.home, name='home'),
    path('restaurant-search/', include('restaurant_search.urls')),
    path('favorites/', include('favorites.urls')),
    path('geolocation/', include('geolocation.urls')),
]