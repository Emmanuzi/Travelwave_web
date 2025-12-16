"""URL configuration for parcels app."""
from django.urls import path
from . import views

app_name = 'parcels'

urlpatterns = [
    path('', views.index, name='index'),
    path('track/', views.track, name='track'),
    # Add more parcel-related URLs here (create, view, etc.)
]

