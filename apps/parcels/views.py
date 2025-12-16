from django.shortcuts import render
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
    """Home page for parcels app."""
    # #region agent log
    _log_debug('debug-session', 'run1', 'A', 'apps/parcels/views.py:index', 'View entry', {'method': request.method, 'path': request.path})
    # #endregion
    template_name = 'parcels/index.html'
    # #region agent log
    _log_debug('debug-session', 'run1', 'A', 'apps/parcels/views.py:index', 'Before render', {'template': template_name})
    # #endregion
    try:
        response = render(request, template_name)
        # #region agent log
        _log_debug('debug-session', 'run1', 'A', 'apps/parcels/views.py:index', 'Render success', {'template': template_name, 'status': response.status_code})
        # #endregion
        return response
    except Exception as e:
        # #region agent log
        _log_debug('debug-session', 'run1', 'A', 'apps/parcels/views.py:index', 'Render error', {'template': template_name, 'error': str(e), 'error_type': type(e).__name__})
        # #endregion
        raise


def track(request):
    """Placeholder for parcel tracking page - will be implemented in TW-6."""
    # #region agent log
    _log_debug('debug-session', 'run1', 'B', 'apps/parcels/views.py:track', 'View entry', {'method': request.method, 'path': request.path})
    # #endregion
    template_name = 'parcels/track.html'
    context = {'message': 'Parcel tracking functionality coming soon!'}
    # #region agent log
    _log_debug('debug-session', 'run1', 'B', 'apps/parcels/views.py:track', 'Before render', {'template': template_name, 'context_keys': list(context.keys())})
    # #endregion
    try:
        response = render(request, template_name, context)
        # #region agent log
        _log_debug('debug-session', 'run1', 'B', 'apps/parcels/views.py:track', 'Render success', {'template': template_name})
        # #endregion
        return response
    except Exception as e:
        # #region agent log
        _log_debug('debug-session', 'run1', 'B', 'apps/parcels/views.py:track', 'Render error', {'template': template_name, 'error': str(e), 'error_type': type(e).__name__})
        # #endregion
        raise