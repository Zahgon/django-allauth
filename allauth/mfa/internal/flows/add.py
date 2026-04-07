from functools import wraps

from django.contrib import messages
from django.contrib.auth.base_user import AbstractBaseUser
from django.core.exceptions import ValidationError
from django.http import HttpResponseRedirect
from django.urls import reverse

from allauth.account.adapter import get_adapter as get_account_adapter
from allauth.account.models import EmailAddress
from allauth.mfa import app_settings
from allauth.mfa.adapter import get_adapter


def validate_can_add_authenticator(user: AbstractBaseUser) -> None:
    """
    If we would allow users to enable 2FA with unverified email address,
    that would allow for an attacker to signup, not verify and prevent the real
    owner of the account from ever regaining access.
    """
    if app_settings.ALLOW_UNVERIFIED_EMAIL:
        return
    email_verified = not EmailAddress.objects.filter(
        user_id=user.pk, verified=False
    ).exists()
    if not email_verified:
        raise get_adapter().validation_error("unverified_email")


def redirect_if_add_not_allowed(function=None):
    pass
