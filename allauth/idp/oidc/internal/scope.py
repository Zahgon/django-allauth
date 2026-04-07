from allauth.idp.oidc.models import Token


def _is_scope_granted(
    scope: str | list[str] | list[list[str]],
    granted_scope: list[str],
) -> bool:
    pass


def is_scope_granted(
    scope: (
        None
        | str
        | list[str]
        | list[list[str]]
        | dict[str, str | list[str] | list[list[str]]]
    ),
    token: Token,
    method: str | None = None,
) -> bool:
    pass
