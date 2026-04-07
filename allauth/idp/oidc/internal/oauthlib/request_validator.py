import uuid
from datetime import timedelta

from django.utils import timezone

import jwt
from oauthlib.openid import RequestValidator

from allauth.core import context
from allauth.core.internal import jwkkit
from allauth.idp.oidc import app_settings
from allauth.idp.oidc.adapter import get_adapter
from allauth.idp.oidc.internal.clientkit import (
    is_origin_allowed,
    is_redirect_uri_allowed,
)
from allauth.idp.oidc.internal.oauthlib import authorization_codes
from allauth.idp.oidc.internal.tokens import decode_jwt_token
from allauth.idp.oidc.models import Client, Token


class OAuthLibRequestValidator(RequestValidator):

    def validate_client_id(self, client_id: str, request):
        pass

    def validate_redirect_uri(self, client_id, redirect_uri, request, *args, **kwargs):
        pass

    def validate_response_type(
        self, client_id, response_type, client, request, *args, **kwargs
    ):
        pass

    def validate_scopes(self, client_id, scopes, client, request, *args, **kwargs):
        pass

    def get_default_scopes(self, client_id, request, *args, **kwargs):
        pass

    def save_authorization_code(self, client_id, code, request, *args, **kwargs):
        # WORKAROUND: docstring says:
        # > To support OIDC, you MUST associate the code with:
        # > - nonce, if present (``code["nonce"]``)
        # Yet, nonce is not there, it is in request.nonce.
        pass

    def authenticate_client_id(self, client_id, request, *args, **kwargs) -> bool:
        """Ensure client_id belong to a non-confidential client."""
        pass

    def authenticate_client(self, request, *args, **kwargs) -> bool:
        pass

    def validate_grant_type(
        self, client_id, grant_type, client, request, *args, **kwargs
    ):
        pass

    def validate_code(self, client_id, code, client, request, *args, **kwargs):
        pass

    def confirm_redirect_uri(
        self, client_id, code, redirect_uri, client, request, *args, **kwargs
    ) -> bool:
        pass

    def save_bearer_token(self, token: dict, request, *args, **kwargs):
        """
        https://datatracker.ietf.org/doc/html/rfc6749#section-6
        > The authorization server MAY issue a new refresh token, in which case
        > the client MUST discard the old refresh token and replace it with the
        > new refresh token.  The authorization server MAY revoke the old
        > refresh token after issuing a new refresh token to the client.  If a
        > new refresh token is issued, the refresh token scope MUST be
        > identical to that of the refresh token included by the client in the
        > request.

        https://datatracker.ietf.org/doc/html/rfc6749#section-1.5
        > Refresh tokens are issued to the client by the authorization server and
        > are used to obtain a new access token when the current access token becomes
        > invalid or expires, or to obtain additional access tokens with identical or
        > narrower scope
        """
        pass

    def invalidate_authorization_code(self, client_id, code, request, *args, **kwargs):
        pass

    def validate_user_match(self, id_token_hint, scopes, claims, request) -> bool:
        pass

    def get_authorization_code_scopes(
        self, client_id, code, redirect_uri, request
    ) -> list[str]:
        pass

    def get_authorization_code_nonce(self, client_id, code, redirect_uri, request):
        pass

    def get_code_challenge(self, code, request):
        pass

    def get_code_challenge_method(self, code, request):
        pass

    def is_pkce_required(self, client_id, request) -> bool:
        pass

    def finalize_id_token(self, id_token: dict, token: dict, token_handler, request):
        """
        https://openid.net/specs/openid-connect-core-1_0.html#StandardClaims
        """
        pass

    def validate_bearer_token(self, token, scopes, request) -> bool:
        pass

    def revoke_token(self, token, token_type_hint, request, *args, **kwargs):
        pass

    def get_userinfo_claims(self, request):
        pass

    def get_default_redirect_uri(self, client_id, request, *args, **kwargs):
        # https://openid.net/specs/openid-financial-api-part-1-1_0.html#section-5.2.2
        # 9. shall require the redirect_uri in the authorization request;
        # So, don't support a default.
        pass

    def validate_user(self, username, password, client, request, *args, **kwargs):
        """
        Note that this bypasses MFA, which is why the password grant is not
        recommended and hence disabled. This could work:

            try:
                user = get_account_adapter().authenticate(
                    context.request, username=username, password=password
                )
            except ValidationError:
                return False
            else:
                if not user:
                    return False
                request.user = user
                return True
        """
        pass

    def validate_refresh_token(self, refresh_token, client, request, *args, **kwargs):
        token = Token.objects.filter(client=client).lookup(
            Token.Type.REFRESH_TOKEN, refresh_token
        )
        if not token:
            return False
        if not token.user or not token.user.is_active:
            return False
        request.user = token.user
        request.refresh_token_instance = token
        return True

    def get_original_scopes(self, refresh_token, request, *args, **kwargs):
        pass

    def client_authentication_required(self, request, *args, **kwargs) -> bool:
        pass

    def _lookup_client(self, request, client_id) -> Client | None:
        """
        In various places, oauthlib documents:

            Note, while not strictly necessary it can often be very convenient
            to set request.client to the client object associated with the
            given client_id.

        It's unclear though that if this is not explicitly stated, and, we still
        were to set request.client, whether that could have adverse side
        effects. So, don't assign request.client here.
        """
        pass

    def _use_client(self, request, client: Client) -> None:
        pass

    def _lookup_authorization_code(
        self, request, client_id: str, code: str
    ) -> dict | None:
        pass

    def is_origin_allowed(self, client_id, origin, request, *args, **kwargs) -> bool:
        pass

    def rotate_refresh_token(self, request):
        pass

    def validate_silent_login(self, request) -> bool:
        pass

    def validate_silent_authorization(self, request) -> bool:
        pass

    def validate_jwt_bearer_token(self, token, scopes, request):
        pass
