from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm
from django.contrib import messages
import json
from pathlib import Path

from .models import Profile
from .forms import ProfileForm

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
            "timestamp": __import__('time').time() * 1000,
        }
        with open(LOG_PATH, 'a', encoding='utf-8') as f:
            f.write(json.dumps(log_entry) + '\n')
    except Exception:
        pass


def _get_or_create_profile(user):
    """Return a Profile instance for the given user, creating it if needed."""
    profile, _ = Profile.objects.get_or_create(user=user)
    return profile


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
    """Display the authenticated user's profile and basic account info."""
    # #region agent log
    _log_debug(
        'debug-session',
        'run1',
        'B',
        'apps/users/views.py:profile',
        'View entry',
        {
            'method': request.method,
            'path': request.path,
            'user': request.user.username if request.user.is_authenticated else 'anonymous',
        },
    )
    # #endregion
    template_name = 'users/profile.html'
    profile = _get_or_create_profile(request.user)
    context = {'user': request.user, 'profile': profile}
    # #region agent log
    _log_debug(
        'debug-session',
        'run1',
        'B',
        'apps/users/views.py:profile',
        'Before render',
        {'template': template_name, 'context_keys': list(context.keys())},
    )
    # #endregion
    try:
        response = render(request, template_name, context)
        # #region agent log
        _log_debug(
            'debug-session',
            'run1',
            'B',
            'apps/users/views.py:profile',
            'Render success',
            {'template': template_name},
        )
        # #endregion
        return response
    except Exception as e:
        # #region agent log
        _log_debug(
            'debug-session',
            'run1',
            'B',
            'apps/users/views.py:profile',
            'Render error',
            {'template': template_name, 'error': str(e), 'error_type': type(e).__name__},
        )
        # #endregion
        raise


@login_required
def edit_profile(request):
    """Allow the authenticated user to update their profile details."""
    profile = _get_or_create_profile(request.user)
    # #region agent log
    _log_debug(
        'debug-session',
        'run1',
        'B',
        'apps/users/views.py:edit_profile',
        'View entry',
        {'method': request.method, 'path': request.path, 'user': request.user.username},
    )
    # #endregion

    if request.method == 'POST':
        form = ProfileForm(request.POST, instance=profile)
        if form.is_valid():
            form.save()
            messages.success(request, 'Your profile has been updated.')
            return redirect('users:profile')
    else:
        form = ProfileForm(instance=profile)

    template_name = 'users/profile_edit.html'
    context = {'form': form}
    # #region agent log
    _log_debug(
        'debug-session',
        'run1',
        'B',
        'apps/users/views.py:edit_profile',
        'Before render',
        {'template': template_name, 'form_valid': form.is_valid() if request.method == 'POST' else None},
    )
    # #endregion
    try:
        response = render(request, template_name, context)
        # #region agent log
        _log_debug(
            'debug-session',
            'run1',
            'B',
            'apps/users/views.py:edit_profile',
            'Render success',
            {'template': template_name},
        )
        # #endregion
        return response
    except Exception as e:
        # #region agent log
        _log_debug(
            'debug-session',
            'run1',
            'B',
            'apps/users/views.py:edit_profile',
            'Render error',
            {'template': template_name, 'error': str(e), 'error_type': type(e).__name__},
        )
        # #endregion
        raise