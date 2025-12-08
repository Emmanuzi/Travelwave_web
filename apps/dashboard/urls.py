"""URL configuration for dashboard app."""
from django.urls import path
from . import views

app_name = 'dashboard'

urlpatterns = [
    path('', views.index, name='index'),
    # Add more dashboard-related URLs here (stats, reports, etc.)
]

