from datetime import timedelta


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
    def ALLOW_UNVERIFIED_EMAIL(self) -> bool:
        pass

    @property
    def FORMS(self) -> dict:
        pass

    @property
    def RECOVERY_CODE_COUNT(self) -> int:
        """
        The number of recovery codes.
        """
        pass

    @property
    def RECOVERY_CODE_DIGITS(self) -> int:
        """
        The number of digits of each recovery code.
        """
        pass

    @property
    def TOTP_PERIOD(self) -> int:
        """
        The period that a TOTP code will be valid for, in seconds.
        """
        pass

    @property
    def TOTP_DIGITS(self) -> int:
        """
        The number of digits for TOTP codes
        """
        pass

    @property
    def TOTP_ISSUER(self) -> str:
        """
        The issuer.
        """
        pass

    @property
    def TOTP_INSECURE_BYPASS_CODE(self):
        """
        Don't use this on production. Useful for development & E2E tests only.
        """
        pass

    @property
    def TOTP_TOLERANCE(self) -> int:
        """
        The number of time steps in the past or future to allow. Lower values are more secure, but more likely to fail due to clock drift.
        """
        pass

    @property
    def SUPPORTED_TYPES(self) -> list[str]:
        pass

    @property
    def WEBAUTHN_ALLOW_INSECURE_ORIGIN(self) -> bool:
        pass

    @property
    def PASSKEY_LOGIN_ENABLED(self) -> bool:
        pass

    @property
    def PASSKEY_SIGNUP_ENABLED(self) -> bool:
        pass

    @property
    def TRUST_ENABLED(self) -> bool:
        pass

    @property
    def _TRUST_STAGE_ENABLED(self) -> bool:
        pass

    @property
    def TRUST_COOKIE_AGE(self) -> timedelta:
        pass

    @property
    def TRUST_COOKIE_NAME(self) -> str:
        pass

    @property
    def TRUST_COOKIE_DOMAIN(self) -> str | None:
        pass

    @property
    def TRUST_COOKIE_HTTPONLY(self) -> bool:
        pass

    @property
    def TRUST_COOKIE_PATH(self) -> str:
        pass

    @property
    def TRUST_COOKIE_SAMESITE(self) -> str:
        pass

    @property
    def TRUST_COOKIE_SECURE(self) -> str | None:
        pass


_app_settings = AppSettings("MFA_")


def __getattr__(name):
    # See https://peps.python.org/pep-0562/
    return getattr(_app_settings, name)
