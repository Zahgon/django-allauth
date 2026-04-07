from functools import wraps

from django.conf import settings
from django.contrib.auth import REDIRECT_FIELD_NAME
from django.contrib.auth.decorators import login_required
from django.core.exceptions import PermissionDenied
from django.http import HttpResponseRedirect
from django.shortcuts import render, resolve_url
from django.urls import reverse

from allauth.account import app_settings
from allauth.account.internal.flows import reauthentication
from allauth.account.internal.flows.email_verification import (
    send_verification_email_for_user,
)
from allauth.account.models import EmailAddress
from allauth.account.utils import get_next_redirect_url
from allauth.core.exceptions import ReauthenticationRequired
from allauth.core.internal import httpkit


def verified_email_required(
    function=None, login_url=None, redirect_field_name=REDIRECT_FIELD_NAME
):
    """
    Even when email verification is not mandatory during signup, there
    may be circumstances during which you really want to prevent
    unverified users to proceed. This decorator ensures the user is
    authenticated and has a verified email address. If the former is
    not the case then the behavior is identical to that of the
    standard `login_required` decorator. If the latter does not hold,
    email verification mails are automatically resend and the user is
    presented with a page informing them they needs to verify their email
    address.
    """
    pass


def reauthentication_required(
    function=None,
    redirect_field_name=REDIRECT_FIELD_NAME,
    allow_get=False,
    enabled=None,
):
    pass


def secure_admin_login(function=None):
    def decorator(view_func):
        @wraps(view_func)
        def _wrapper_view(request, *args, **kwargs):
            pass

        return _wrapper_view

    if function:
        return decorator(function)
    return decorator
