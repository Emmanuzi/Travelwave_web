from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm
from django.contrib import messages
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
    """Home page for users app."""
    # #region agent log
    _log_debug('debug-session', 'run1', 'A', 'apps/users/views.py:index', 'View entry', {'method': request.method, 'path': request.path})
    # #endregion
    template_name = 'users/index.html'
    # #region agent log
    _log_debug('debug-session', 'run1', 'A', 'apps/users/views.py:index', 'Before render', {'template': template_name})
    # #endregion
    try:
        response = render(request, template_name)
        # #region agent log
        _log_debug('debug-session', 'run1', 'A', 'apps/users/views.py:index', 'Render success', {'template': template_name, 'status': response.status_code})
        # #endregion
        return response
    except Exception as e:
        # #region agent log
        _log_debug('debug-session', 'run1', 'A', 'apps/users/views.py:index', 'Render error', {'template': template_name, 'error': str(e), 'error_type': type(e).__name__})
        # #endregion
        raise


def register(request):
    """Placeholder for registration page - will be implemented in TW-3."""
    # #region agent log
    _log_debug('debug-session', 'run1', 'B', 'apps/users/views.py:register', 'View entry', {'method': request.method, 'path': request.path})
    # #endregion
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        # #region agent log
        _log_debug('debug-session', 'run1', 'B', 'apps/users/views.py:register', 'Form created', {'is_valid': form.is_valid()})
        # #endregion
        if form.is_valid():
            form.save()
            messages.success(request, 'Registration successful! Please login.')
            # #region agent log
            _log_debug('debug-session', 'run1', 'B', 'apps/users/views.py:register', 'Redirecting to login', {})
            # #endregion
            return redirect('users:login')
    else:
        form = UserCreationForm()
    template_name = 'users/register.html'
    # #region agent log
    _log_debug('debug-session', 'run1', 'B', 'apps/users/views.py:register', 'Before render', {'template': template_name})
    # #endregion
    try:
        response = render(request, template_name, {'form': form})
        # #region agent log
        _log_debug('debug-session', 'run1', 'B', 'apps/users/views.py:register', 'Render success', {'template': template_name})
        # #endregion
        return response
    except Exception as e:
        # #region agent log
        _log_debug('debug-session', 'run1', 'B', 'apps/users/views.py:register', 'Render error', {'template': template_name, 'error': str(e), 'error_type': type(e).__name__})
        # #endregion
        raise


@login_required
def profile(request):
    """Placeholder for profile page - will be implemented in TW-3."""
    # #region agent log
    _log_debug('debug-session', 'run1', 'B', 'apps/users/views.py:profile', 'View entry', {'method': request.method, 'path': request.path, 'user': request.user.username if request.user.is_authenticated else 'anonymous'})
    # #endregion
    template_name = 'users/profile.html'
    context = {'user': request.user}
    # #region agent log
    _log_debug('debug-session', 'run1', 'B', 'apps/users/views.py:profile', 'Before render', {'template': template_name, 'context_keys': list(context.keys())})
    # #endregion
    try:
        response = render(request, template_name, context)
        # #region agent log
        _log_debug('debug-session', 'run1', 'B', 'apps/users/views.py:profile', 'Render success', {'template': template_name})
        # #endregion
        return response
    except Exception as e:
        # #region agent log
        _log_debug('debug-session', 'run1', 'B', 'apps/users/views.py:profile', 'Render error', {'template': template_name, 'error': str(e), 'error_type': type(e).__name__})
        # #endregion
        raise