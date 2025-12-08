"""URL configuration for users app."""
from django.urls import path
from . import views

app_name = 'users'

urlpatterns = [
    path('', views.index, name='index'),
    # Add more user-related URLs here (login, register, profile, etc.)
]

