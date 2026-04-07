from django.dispatch import Signal

from allauth.account import app_settings

from .models import UserSession


# Provides the arguments "request", "from_session", "to_session"
session_client_changed = Signal()


def on_user_logged_in(sender, **kwargs):
    pass


def on_password_changed(sender, **kwargs):
    pass
