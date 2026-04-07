import jwt

from allauth.core.internal import jwkkit
from allauth.idp.oidc import app_settings
from allauth.idp.oidc.adapter import get_adapter


def decode_jwt_token(
    value: str, *, client_id: str | None = None, verify_exp: bool, verify_iss: bool
) -> dict | None:
    pass
