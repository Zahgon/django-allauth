import re
from re import Pattern
from urllib.parse import ParseResult, parse_qsl, urlparse

from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _

from allauth.idp.oidc.models import Client


def is_loopback(parsed_uri: ParseResult) -> bool:
    pass


def _validate_uri_wildcard_format(uri: str, allow_uri_wildcards: bool) -> None:
    if not allow_uri_wildcards:
        if "*" in uri:
            raise ValidationError(
                _("Wildcards are not allowed unless 'Allow URI wildcards' is enabled.")
            )
    elif uri.count("*") > 1:
        raise ValidationError(
            _(
                "URI '{}' contains more than one wildcard (*). Only one wildcard per URI is allowed."
            ).format(uri)
        )
    else:
        try:
            parsed = urlparse(uri)
        except ValueError as e:
            # it's possible for this to happen with wildcards in ports
            raise ValidationError(_(f"Invalid URI: {e}"))

        if "*" in parsed.scheme or "*" in parsed.path or "*" in parsed.query:
            raise ValidationError(
                _("Wildcards are only allowed in the hostname portion of the URI.")
            )


def _wildcard_to_regex(wildcard: str) -> Pattern:
    pass


def _is_scheme_hostname_allowed(
    parsed_uri: ParseResult, parsed_allowed_uri: ParseResult, allow_uri_wildcards: bool
) -> bool:
    pass


def is_parsed_redirect_uri_allowed(
    parsed_uri: ParseResult, allowed_uri: str, allow_uri_wildcards: bool
) -> bool:
    pass


def is_redirect_uri_allowed(
    uri: str, allowed_uris: list[str], allow_uri_wildcards: bool
) -> bool:
    pass


def is_origin_allowed(
    origin: str, allowed_origins: list[str], allow_uri_wildcards: bool
) -> bool:
    pass


def get_used_schemes(client: Client) -> set[str]:
    schemes = set()
    for uri in client.get_redirect_uris():
        parsed = urlparse(uri)
        if parsed.scheme:
            schemes.add(parsed.scheme)
    return schemes


def clean_post_logout_redirect_uri(
    post_logout_redirect_uri: str | None, client: Client | None
) -> str | None:
    """
    This URI SHOULD use the https scheme and MAY contain port, path, and
    query parameter components; however, it MAY use the http scheme, provided
    that the Client Type is confidential, as defined in Section 2.1 of OAuth 2.0
    [RFC6749], and provided the OP allows the use of http RP URIs. The URI MAY
    use an alternate scheme, such as one that is intended to identify a callback
    into a native application. The value MUST have been previously registered
    with the OP, either using the post_logout_redirect_uris Registration
    parameter or via another mechanism. An id_token_hint is also RECOMMENDED
    when this parameter is included.
    """
    allowed_schemes = {"https"}
    if client:
        allowed_schemes.update(get_used_schemes(client))
        if client.type == Client.Type.CONFIDENTIAL:
            allowed_schemes.add("http")
    parsed = urlparse(post_logout_redirect_uri)
    if not parsed.scheme or parsed.scheme not in allowed_schemes:
        return None
    return post_logout_redirect_uri
