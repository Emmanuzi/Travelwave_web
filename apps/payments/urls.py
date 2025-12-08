"""URL configuration for payments app."""
from django.urls import path
from . import views

app_name = 'payments'

urlpatterns = [
    path('', views.index, name='index'),
    # Add more payment-related URLs here (process, success, failure, etc.)
]

