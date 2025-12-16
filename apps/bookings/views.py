from django.shortcuts import render
from django.contrib.auth.decorators import login_required
import json
from pathlib import Path

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
    """Placeholder for booking search page - will be implemented in TW-5."""
    # #region agent log
    _log_debug('debug-session', 'run1', 'B', 'apps/bookings/views.py:search', 'View entry', {'method': request.method, 'path': request.path})
    # #endregion
    template_name = 'bookings/search.html'
    context = {'message': 'Booking search functionality coming soon!'}
    # #region agent log
    _log_debug('debug-session', 'run1', 'B', 'apps/bookings/views.py:search', 'Before render', {'template': template_name, 'context_keys': list(context.keys())})
    # #endregion
    try:
        response = render(request, template_name, context)
        # #region agent log
        _log_debug('debug-session', 'run1', 'B', 'apps/bookings/views.py:search', 'Render success', {'template': template_name})
        # #endregion
        return response
    except Exception as e:
        # #region agent log
        _log_debug('debug-session', 'run1', 'B', 'apps/bookings/views.py:search', 'Render error', {'template': template_name, 'error': str(e), 'error_type': type(e).__name__})
        # #endregion
        raise


@login_required
def my_bookings(request):
    """Placeholder for user bookings page - will be implemented in TW-5."""
    # #region agent log
    _log_debug('debug-session', 'run1', 'B', 'apps/bookings/views.py:my_bookings', 'View entry', {'method': request.method, 'path': request.path, 'user': request.user.username if request.user.is_authenticated else 'anonymous'})
    # #endregion
    template_name = 'bookings/my_bookings.html'
    context = {'message': 'My bookings page coming soon!'}
    # #region agent log
    _log_debug('debug-session', 'run1', 'B', 'apps/bookings/views.py:my_bookings', 'Before render', {'template': template_name, 'context_keys': list(context.keys())})
    # #endregion
    try:
        response = render(request, template_name, context)
        # #region agent log
        _log_debug('debug-session', 'run1', 'B', 'apps/bookings/views.py:my_bookings', 'Render success', {'template': template_name})
        # #endregion
        return response
    except Exception as e:
        # #region agent log
        _log_debug('debug-session', 'run1', 'B', 'apps/bookings/views.py:my_bookings', 'Render error', {'template': template_name, 'error': str(e), 'error_type': type(e).__name__})
        # #endregion
        raise