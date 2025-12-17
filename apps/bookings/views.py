from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.db import transaction
from django.utils import timezone
import json
from pathlib import Path

from .models import Route, Schedule, Seat, Booking

# Create your views here.

# #region agent log
LOG_PATH = Path(__file__).resolve().parent.parent.parent / '.cursor' / 'debug.log'
# #endregion

def _log_debug(session_id, run_id, hypothesis_id, location, message, data):
    """Helper to write debug logs in NDJSON format."""
    try:
        log_entry = {
            "sessionId": session_id,
            "runId": run_id,
            "hypothesisId": hypothesis_id,
            "location": location,
            "message": message,
            "data": data,
            "timestamp": __import__('time').time() * 1000
        }
        with open(LOG_PATH, 'a', encoding='utf-8') as f:
            f.write(json.dumps(log_entry) + '\n')
    except Exception:
        pass

def index(request):
    """Home page for bookings app."""
    # #region agent log
    _log_debug('debug-session', 'run1', 'A', 'apps/bookings/views.py:index', 'View entry', {'method': request.method, 'path': request.path})
    # #endregion
    template_name = 'bookings/index.html'
    # #region agent log
    _log_debug('debug-session', 'run1', 'A', 'apps/bookings/views.py:index', 'Before render', {'template': template_name})
    # #endregion
    try:
        response = render(request, template_name)
        # #region agent log
        _log_debug('debug-session', 'run1', 'A', 'apps/bookings/views.py:index', 'Render success', {'template': template_name, 'status': response.status_code})
        # #endregion
        return response
    except Exception as e:
        # #region agent log
        _log_debug('debug-session', 'run1', 'A', 'apps/bookings/views.py:index', 'Render error', {'template': template_name, 'error': str(e), 'error_type': type(e).__name__})
        # #endregion
        raise


def search(request):
    """Search for schedules by origin, destination, and date."""
    _log_debug('debug-session', 'run1', 'B', 'apps/bookings/views.py:search', 'View entry', {'method': request.method, 'path': request.path})
    template_name = 'bookings/search.html'
    origin = request.GET.get('origin', '').strip()
    destination = request.GET.get('destination', '').strip()
    date_str = request.GET.get('date', '').strip()

    schedules = []
    selected_date = None
    if date_str:
        try:
            selected_date = timezone.datetime.strptime(date_str, "%Y-%m-%d").date()
        except ValueError:
            selected_date = None

    if origin or destination or selected_date:
        qs = Schedule.objects.select_related('route', 'bus', 'bus__company').filter(status=Schedule.ACTIVE)
        if origin:
            qs = qs.filter(route__origin__icontains=origin)
        if destination:
            qs = qs.filter(route__destination__icontains=destination)
        if selected_date:
            qs = qs.filter(departure_time__date=selected_date)
        schedules = qs.order_by('departure_time')

    context = {
        'origin': origin,
        'destination': destination,
        'date': date_str,
        'schedules': schedules,
    }
    _log_debug('debug-session', 'run1', 'B', 'apps/bookings/views.py:search', 'Before render', {'template': template_name, 'context_keys': list(context.keys())})
    try:
        response = render(request, template_name, context)
        _log_debug('debug-session', 'run1', 'B', 'apps/bookings/views.py:search', 'Render success', {'template': template_name})
        return response
    except Exception as e:
        _log_debug('debug-session', 'run1', 'B', 'apps/bookings/views.py:search', 'Render error', {'template': template_name, 'error': str(e), 'error_type': type(e).__name__})
        raise


@login_required
def my_bookings(request):
    """List bookings for the authenticated user."""
    _log_debug('debug-session', 'run1', 'B', 'apps/bookings/views.py:my_bookings', 'View entry', {'method': request.method, 'path': request.path, 'user': request.user.username if request.user.is_authenticated else 'anonymous'})
    template_name = 'bookings/my_bookings.html'
    bookings = Booking.objects.select_related('schedule', 'schedule__route', 'schedule__bus', 'schedule__bus__company').prefetch_related('seats').filter(user=request.user)
    context = {'bookings': bookings}
    _log_debug('debug-session', 'run1', 'B', 'apps/bookings/views.py:my_bookings', 'Before render', {'template': template_name, 'context_keys': list(context.keys())})
    try:
        response = render(request, template_name, context)
        _log_debug('debug-session', 'run1', 'B', 'apps/bookings/views.py:my_bookings', 'Render success', {'template': template_name})
        return response
    except Exception as e:
        _log_debug('debug-session', 'run1', 'B', 'apps/bookings/views.py:my_bookings', 'Render error', {'template': template_name, 'error': str(e), 'error_type': type(e).__name__})
        raise


@login_required
def schedule_detail(request, schedule_id):
    """Show schedule details and allow seat selection/booking."""
    schedule = get_object_or_404(
        Schedule.objects.select_related('route', 'bus', 'bus__company').prefetch_related('seats'),
        id=schedule_id,
        status=Schedule.ACTIVE,
    )
    template_name = 'bookings/schedule_detail.html'

    # Available seats
    seats = schedule.seats.all().order_by('seat_number')
    selected_seat_numbers = request.POST.getlist('seats')

    if request.method == 'POST':
        if not selected_seat_numbers:
            messages = {'error': 'Please select at least one seat.'}
            return render(request, template_name, {'schedule': schedule, 'seats': seats, 'messages_dict': messages})

        with transaction.atomic():
            # Lock seats to prevent race conditions
            seats_to_book = (
                Seat.objects.select_for_update()
                .filter(schedule=schedule, seat_number__in=selected_seat_numbers, status=Seat.AVAILABLE)
                .order_by('seat_number')
            )
            if seats_to_book.count() != len(selected_seat_numbers):
                messages = {'error': 'One or more selected seats are no longer available. Please refresh and try again.'}
                return render(request, template_name, {'schedule': schedule, 'seats': seats, 'messages_dict': messages})

            total_price = schedule.price * len(selected_seat_numbers)
            booking = Booking.objects.create(
                user=request.user,
                schedule=schedule,
                total_price=total_price,
                status=Booking.CONFIRMED,
            )
            booking.seats.add(*seats_to_book)
            seats_to_book.update(status=Seat.BOOKED)

        return redirect('bookings:my_bookings')

    return render(request, template_name, {'schedule': schedule, 'seats': seats})