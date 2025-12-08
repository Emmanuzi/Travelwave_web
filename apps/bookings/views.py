from django.shortcuts import render

# Create your views here.


def index(request):
    """Home page for bookings app."""
    return render(request, 'bookings/index.html')