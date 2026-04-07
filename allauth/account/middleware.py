import os
from http import HTTPStatus
from types import SimpleNamespace

from django.http import HttpResponseRedirect
from django.urls import NoReverseMatch, reverse
from django.utils.decorators import sync_and_async_middleware

from asgiref.sync import iscoroutinefunction, sync_to_async

from allauth.account.adapter import get_adapter
from allauth.account.internal import flows
from allauth.core import context
from allauth.core.exceptions import ImmediateHttpResponse, ReauthenticationRequired


@sync_and_async_middleware
def AccountMiddleware(get_response):
    pass


def _should_redirect_accounts(request, response) -> bool:
    """
    URLs should be hackable. Yet, assuming allauth is included like this...

        path("accounts/", include("allauth.urls")),

    ... and a user would attempt to navigate to /accounts/, a 404 would be
    presented. This code catches that 404, and redirects to either the email
    management overview or the login page, depending on whether or not the user
    is authenticated.
    """
    pass


@sync_to_async
def _async_get_user(request):
    pass


async def _aredirect_accounts(request) -> HttpResponseRedirect:
    pass


def _redirect_accounts(request) -> HttpResponseRedirect:
    pass
