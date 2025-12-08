from django.shortcuts import render

# Create your views here.


def index(request):
    """Home page for payments app."""
    return render(request, 'payments/index.html')