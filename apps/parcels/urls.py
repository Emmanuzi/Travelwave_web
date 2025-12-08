"""URL configuration for parcels app."""
from django.urls import path
from . import views

app_name = 'parcels'

urlpatterns = [
    path('', views.index, name='index'),
    # Add more parcel-related URLs here (track, create, view, etc.)
]

