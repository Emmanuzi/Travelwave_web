"""Root views for TravelWave project."""
from django.shortcuts import render
import json
from pathlib import Path

# #region agent log
LOG_PATH = Path(__file__).resolve().parent.parent / '.cursor' / 'debug.log'
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

def home(request):
    """Home page view."""
    # #region agent log
    _log_debug('debug-session', 'run1', 'A', 'travelwave/views.py:home', 'View entry', {'method': request.method, 'path': request.path})
    # #endregion
    template_name = 'home.html'
    # #region agent log
    _log_debug('debug-session', 'run1', 'A', 'travelwave/views.py:home', 'Before render', {'template': template_name})
    # #endregion
    try:
        response = render(request, template_name)
        # #region agent log
        _log_debug('debug-session', 'run1', 'A', 'travelwave/views.py:home', 'Render success', {'template': template_name, 'status': response.status_code})
        # #endregion
        return response
    except Exception as e:
        # #region agent log
        _log_debug('debug-session', 'run1', 'A', 'travelwave/views.py:home', 'Render error', {'template': template_name, 'error': str(e), 'error_type': type(e).__name__})
        # #endregion
        raise

