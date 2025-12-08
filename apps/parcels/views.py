from django.shortcuts import render

# Create your views here.


def index(request):
    """Home page for parcels app."""
    return render(request, 'parcels/index.html')