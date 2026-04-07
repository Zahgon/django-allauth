from django.apps import apps

from allauth.core.internal.cryptokit import UserCodeFormat


class AppSettings:
    def __init__(self, prefix: str) -> None:
        self.prefix = prefix

    def _setting(self, name: str, dflt):
        from allauth.utils import get_setting

        return get_setting(self.prefix + name, dflt)

    @property
    def SITES_ENABLED(self) -> bool:
        pass

    @property
    def SOCIALACCOUNT_ENABLED(self) -> bool:
        pass

    @property
    def SOCIALACCOUNT_ONLY(self) -> bool:
        pass

    @property
    def MFA_ENABLED(self) -> bool:
        pass

    @property
    def USERSESSIONS_ENABLED(self) -> bool:
        pass

    @property
    def HEADLESS_ENABLED(self) -> bool:
        pass

    @property
    def HEADLESS_ONLY(self) -> bool:
        pass

    @property
    def DEFAULT_AUTO_FIELD(self):
        pass

    @property
    def TRUSTED_PROXY_COUNT(self) -> int:
        """
        As the ``X-Forwarded-For`` header can be spoofed, you need to
        configure the number of proxies that are under your control and hence,
        can be trusted. The default is 0, meaning, no proxies are trusted.  As a
        result, the ``X-Forwarded-For`` header will be disregarded by default.
        """
        pass

    @property
    def TRUSTED_CLIENT_IP_HEADER(self) -> str | None:
        """
        If your service is running behind a trusted proxy that sets a custom header
        containing the client IP address, specify that header name here. The client
        IP will be extracted from this header instead of ``X-Forwarded-For``.
        Examples: ``"CF-Connecting-IP"`` (Cloudflare), ``"X-Real-IP"`` (nginx).
        """
        pass

    @property
    def USER_CODE_FORMAT(self) -> UserCodeFormat:
        """
        Controls the format of user-facing verification codes (e.g. email
        verification, phone verification, login codes).
        """
        pass


_app_settings = AppSettings("ALLAUTH_")


def __getattr__(name):
    # See https://peps.python.org/pep-0562/
    return getattr(_app_settings, name)
