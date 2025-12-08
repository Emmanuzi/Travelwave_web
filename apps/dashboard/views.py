from django.shortcuts import render

# Create your views here.


def index(request):
    """Home page for dashboard app."""
    return render(request, 'dashboard/index.html')