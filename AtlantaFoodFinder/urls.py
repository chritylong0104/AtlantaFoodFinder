from django.contrib import admin
from django.urls import path, include
from geolocation import views

urlpatterns = [
    path('', views.home_view, name='home'),  # Add this line
    path('admin/', admin.site.urls),
    path('accounts/', include('user_authentication.urls')),
    path('restaurant-search/', include('restaurant_search.urls')),
    path('favorites/', include('favorites.urls')),
    path('geolocation/', include('geolocation.urls')),
    path('restaurant/<str:place_id>/', views.restaurant_detail, name='restaurant_detail'),
    path('favorites/', include('favorites.urls')),

]