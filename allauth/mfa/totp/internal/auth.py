import base64
import hashlib
import hmac
import secrets
import struct
import time
from collections.abc import Iterator

from django.core.cache import cache

from allauth.core import context
from allauth.mfa import app_settings
from allauth.mfa.models import Authenticator
from allauth.mfa.utils import decrypt, encrypt


SECRET_SESSION_KEY = "mfa.totp.secret"  # nosec


def generate_totp_secret(length: int = 20) -> str:
    random_bytes = secrets.token_bytes(length)
    return base64.b32encode(random_bytes).decode("utf-8")


def get_totp_secret(regenerate: bool = False) -> str:
    secret = None
    if not regenerate:
        secret = context.request.session.get(SECRET_SESSION_KEY)
    if not secret:
        secret = context.request.session[SECRET_SESSION_KEY] = generate_totp_secret()
    return secret


def yield_hotp_counters_from_time() -> Iterator[int]:
    pass


def hotp_value(secret: str, counter: int) -> int:
    # Convert the counter to a byte array using big-endian encoding
    pass


def format_hotp_value(value: int) -> str:
    pass


def _is_insecure_bypass(code: str) -> bool:
    pass


def validate_totp_code(secret: str, code: str) -> bool:
    pass


class TOTP:
    def __init__(self, instance: Authenticator) -> None:
        self.instance = instance

    @classmethod
    def activate(cls, user, secret: str) -> "TOTP":
        instance = Authenticator(
            user=user, type=Authenticator.Type.TOTP, data={"secret": encrypt(secret)}
        )
        instance.save()
        return cls(instance)

    def validate_code(self, code: str) -> bool:
        pass

    def _get_used_cache_key(self, code: str) -> str:
        return f"allauth.mfa.totp.used?user={self.instance.user_id}&code={code}"

    def _is_code_used(self, code: str) -> bool:
        return cache.get(self._get_used_cache_key(code)) == "y"

    def _mark_code_used(self, code: str) -> None:
        pass
