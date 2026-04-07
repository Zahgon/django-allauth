from allauth import app_settings as allauth_settings
from allauth.core.internal.cryptokit import UserCodeFormat


class AppSettings:
    def __init__(self, prefix: str) -> None:
        self.prefix = prefix

    def _setting(self, name: str, dflt):
        from allauth.utils import get_setting

        return get_setting(f"{self.prefix}{name}", dflt)

    @property
    def ADAPTER(self) -> str:
        pass

    @property
    def ID_TOKEN_EXPIRES_IN(self) -> int:
        pass

    @property
    def PRIVATE_KEY(self) -> str:
        pass

    @property
    def ACCESS_TOKEN_EXPIRES_IN(self) -> int:
        pass

    @property
    def ACCESS_TOKEN_FORMAT(self) -> str:
        pass

    @property
    def AUTHORIZATION_CODE_EXPIRES_IN(self) -> int:
        pass

    @property
    def ROTATE_REFRESH_TOKEN(self) -> bool:
        pass

    @property
    def DEVICE_CODE_EXPIRES_IN(self) -> int:
        pass

    @property
    def DEVICE_CODE_INTERVAL(self) -> int:
        pass

    @property
    def USER_CODE_FORMAT(self) -> UserCodeFormat:
        pass

    @property
    def RATE_LIMITS(self) -> dict:
        pass

    @property
    def RP_INITIATED_LOGOUT_ASKS_FOR_OP_LOGOUT(self) -> bool:
        """
        At https://openid.net/specs/openid-connect-rpinitiated-1_0.html

        > 2. RP-Initiated Logout':
        > At the Logout Endpoint, the OP SHOULD ask the End-User whether to
        > log out of the OP as well.

        This setting controls whether the OP always asks.
        """
        pass

    @property
    def USERINFO_ENDPOINT(self) -> str | None:
        """
        This setting can be used to point the ``userinfo_endpoint`` value as
        returned in the ".well-known/openid-configuration" to a custom URL.
        Setting this disables the built-in userinfo endpoint.
        """
        pass


_app_settings = AppSettings("IDP_OIDC_")


def __getattr__(name):
    # See https://peps.python.org/pep-0562/
    return getattr(_app_settings, name)
