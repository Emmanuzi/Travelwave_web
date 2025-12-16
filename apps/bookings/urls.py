"""URL configuration for bookings app."""
from django.urls import path
from . import views

app_name = 'bookings'

urlpatterns = [
    path('', views.index, name='index'),
    path('search/', views.search, name='search'),
    path('my-bookings/', views.my_bookings, name='my_bookings'),
    # Add more booking-related URLs here (book, view bookings, etc.)
]

