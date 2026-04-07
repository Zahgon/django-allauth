class AppSettings:
    def __init__(self, prefix: str) -> None:
        self.prefix = prefix

    def _setting(self, name: str, dflt):
        from allauth.utils import get_setting

        return get_setting(self.prefix + name, dflt)

    @property
    def ADAPTER(self) -> str:
        pass

    @property
    def TOKEN_STRATEGY(self):
        pass

    @property
    def SERVE_SPECIFICATION(self) -> bool:
        pass

    @property
    def SPECIFICATION_TEMPLATE_NAME(self) -> str | None:
        pass

    @property
    def CLIENTS(self) -> tuple[str]:
        pass

    @property
    def FRONTEND_URLS(self) -> dict:
        pass

    @property
    def JWT_ALGORITHM(self) -> str:
        pass

    @property
    def JWT_PRIVATE_KEY(self) -> str:
        pass

    @property
    def JWT_ACCESS_TOKEN_EXPIRES_IN(self) -> int:
        pass

    @property
    def JWT_REFRESH_TOKEN_EXPIRES_IN(self) -> int:
        pass

    @property
    def JWT_AUTHORIZATION_HEADER_SCHEME(self) -> str:
        pass

    @property
    def JWT_STATEFUL_VALIDATION_ENABLED(self) -> bool:
        pass

    @property
    def JWT_ROTATE_REFRESH_TOKEN(self) -> bool:
        pass


_app_settings = AppSettings("HEADLESS_")


def __getattr__(name):
    # See https://peps.python.org/pep-0562/
    return getattr(_app_settings, name)
