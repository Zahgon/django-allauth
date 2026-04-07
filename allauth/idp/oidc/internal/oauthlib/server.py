import secrets
import time
import uuid

from django.urls import reverse

import jwt
from oauthlib.oauth2.rfc8628.endpoints import DeviceApplicationServer
from oauthlib.openid import Server

from allauth.core import context
from allauth.core.internal import jwkkit
from allauth.idp.oidc import app_settings
from allauth.idp.oidc.adapter import get_adapter
from allauth.idp.oidc.internal.oauthlib.request_validator import (
    OAuthLibRequestValidator,
)


def generate_opaque_token(request):
    # 160 bit token is recommended, oauthlib uses less.
    # oauch.io -- at oautlib's default, we get:
    #    Out of 11 valid authorization responses, the
    #    average calculated entropy for the access tokens was 144,3 (±7,1) bits
    pass


def generate_jwt_access_token(request) -> str:
    pass


def generate_access_token(request) -> str:
    pass


def generate_refresh_token(request) -> str:
    pass


class OAuthLibServer(Server):
    def __init__(self, **kwargs):
        super().__init__(
            token_generator=generate_access_token,
            refresh_token_generator=generate_refresh_token,
            request_validator=OAuthLibRequestValidator(),
            token_expires_in=app_settings.ACCESS_TOKEN_EXPIRES_IN,
            **kwargs,
        )


class DeviceOAuthLibServer(DeviceApplicationServer):
    def __init__(self):
        verification_uri = context.request.build_absolute_uri(
            reverse("idp:oidc:device_authorization")
        )
        super().__init__(
            request_validator=OAuthLibRequestValidator(),
            verification_uri=verification_uri,
            verification_uri_complete=f"{verification_uri}?code={{user_code}}",
            interval=app_settings.DEVICE_CODE_INTERVAL,
            user_code_generator=lambda: get_adapter().generate_user_code(),
        )
        self._expires_in = app_settings.DEVICE_CODE_EXPIRES_IN


def get_server(**kwargs):
    return OAuthLibServer(**kwargs)


def get_device_server():
    return DeviceOAuthLibServer()
