class AppSettings:
    def __init__(self, prefix: str) -> None:
        self.prefix = prefix

    def _setting(self, name: str, dflt):
        from allauth.utils import get_setting

        return get_setting(self.prefix + name, dflt)

    @property
    def QUERY_EMAIL(self) -> bool:
        """
        Request email address from 3rd party account provider?
        E.g. using OpenID AX
        """
        pass

    @property
    def AUTO_SIGNUP(self) -> bool:
        """
        Attempt to bypass the signup form by using fields (e.g. username,
        email) retrieved from the social account provider. If a conflict
        arises due to a duplicate email signup form will still kick in.
        """
        pass

    @property
    def PROVIDERS(self) -> dict:
        """
        Provider specific settings
        """
        pass

    def _migrate_oidc(self, oidc: dict) -> dict:
        pass

    @property
    def EMAIL_REQUIRED(self) -> bool:
        """
        The user is required to hand over an email address when signing up
        """
        pass

    @property
    def EMAIL_VERIFICATION(self):
        """
        See email verification method.  When `None`, the default
        `allauth.account` logic kicks in.
        """
        pass

    @property
    def EMAIL_AUTHENTICATION(self) -> bool:
        """Consider a scenario where a social login occurs, and the social
        account comes with a verified email address (verified by the account
        provider), but that email address is already taken by a local user
        account. Additionally, assume that the local user account does not have
        any social account connected. Now, if the provider can be fully trusted,
        you can argue that we should treat this scenario as a login to the
        existing local user account even if the local account does not already
        have the social account connected, because -- according to the provider
        -- the user logging in has ownership of the email address.  This is how
        this scenario is handled when `EMAIL_AUTHENTICATION` is set to
        `True`. As this implies that an untrustworthy provider can login to any
        local account by fabricating social account data, this setting defaults
        to `False`. Only set it to `True` if you are using providers that can be
        fully trusted.
        """
        pass

    @property
    def EMAIL_AUTHENTICATION_AUTO_CONNECT(self) -> bool:
        """In case email authentication is applied, this setting controls
        whether or not the social account is automatically connected to the
        local account. In case of ``False`` (the default) the local account
        remains unchanged during the login. In case of ``True``, the social
        account for which the email matched, is automatically added to the list
        of social accounts connected to the local account. As a result, even if
        the user were to change the email address afterwards, social login
        would still be possible when using ``True``, but not in case of
        ``False``.
        """
        pass

    @property
    def ADAPTER(self) -> str:
        pass

    @property
    def FORMS(self) -> dict:
        pass

    @property
    def LOGIN_ON_GET(self) -> bool:
        pass

    @property
    def STORE_TOKENS(self) -> bool:
        pass

    @property
    def UID_MAX_LENGTH(self) -> int:
        pass

    @property
    def SOCIALACCOUNT_STR(self):
        pass

    @property
    def REQUESTS_TIMEOUT(self) -> int:
        pass

    @property
    def OPENID_CONNECT_URL_PREFIX(self) -> str:
        pass


_app_settings = AppSettings("SOCIALACCOUNT_")


def __getattr__(name):
    # See https://peps.python.org/pep-0562/
    return getattr(_app_settings, name)
