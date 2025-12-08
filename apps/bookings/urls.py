"""URL configuration for bookings app."""
from django.urls import path
from . import views

app_name = 'bookings'

urlpatterns = [
    path('', views.index, name='index'),
    # Add more booking-related URLs here (search, book, view bookings, etc.)
]

