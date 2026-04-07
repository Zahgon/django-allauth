import warnings
from enum import Enum

from allauth import app_settings as allauth_settings
from allauth.core.internal.cryptokit import UserCodeFormat


class AppSettings:
    class AuthenticationMethod(str, Enum):
        USERNAME = "username"
        EMAIL = "email"
        USERNAME_EMAIL = "username_email"

    class LoginMethod(str, Enum):
        USERNAME = "username"
        EMAIL = "email"
        PHONE = "phone"

    class EmailVerificationMethod(str, Enum):
        # After signing up, keep the user account inactive until the email
        # address is verified
        MANDATORY = "mandatory"
        # Allow login with unverified email (email verification is
        # still sent)
        OPTIONAL = "optional"
        # Don't send email verification mails during signup
        NONE = "none"

    def __init__(self, prefix):
        self.prefix = prefix

    def _setting(self, name, dflt):
        from allauth.utils import get_setting

        return get_setting(self.prefix + name, dflt)

    @property
    def PREVENT_ENUMERATION(self):
        pass

    @property
    def DEFAULT_HTTP_PROTOCOL(self):
        pass

    @property
    def EMAIL_CONFIRMATION_EXPIRE_DAYS(self):
        """
        Determines the expiration date of email confirmation mails (#
        of days)
        """
        pass

    @property
    def EMAIL_CONFIRMATION_AUTHENTICATED_REDIRECT_URL(self):
        """
        The URL to redirect to after a successful email confirmation, in
        case of an authenticated user
        """
        pass

    @property
    def EMAIL_CONFIRMATION_ANONYMOUS_REDIRECT_URL(self):
        """
        The URL to redirect to after a successful email confirmation, in
        case no user is logged in
        """
        pass

    @property
    def EMAIL_REQUIRED(self):
        """
        The user is required to hand over an email address when signing up
        """
        pass

    @property
    def EMAIL_VERIFICATION(self):
        """
        See email verification method
        """
        pass

    @property
    def EMAIL_VERIFICATION_BY_CODE_ENABLED(self):
        pass

    @property
    def EMAIL_VERIFICATION_BY_CODE_MAX_ATTEMPTS(self):
        pass

    @property
    def EMAIL_VERIFICATION_BY_CODE_TIMEOUT(self):
        pass

    @property
    def EMAIL_VERIFICATION_MAX_CHANGE_COUNT(self) -> int:
        """
        The maximum number of times the email can be changed after signup at
        the email veriication stage.
        """
        pass

    @property
    def EMAIL_VERIFICATION_MAX_RESEND_COUNT(self) -> int:
        """
        The maximum number of times the user can request a new email verification code.
        """
        pass

    @property
    def MAX_EMAIL_ADDRESSES(self):
        pass

    @property
    def CHANGE_EMAIL(self):
        pass

    @property
    def AUTHENTICATION_METHOD(self):
        pass

    @property
    def LOGIN_METHODS(self) -> frozenset[LoginMethod]:
        pass

    @property
    def EMAIL_MAX_LENGTH(self):
        """
        Adjust max_length of email addresses
        """
        pass

    @property
    def PHONE_VERIFICATION_ENABLED(self):
        pass

    @property
    def PHONE_VERIFICATION_MAX_ATTEMPTS(self):
        pass

    @property
    def PHONE_VERIFICATION_MAX_CHANGE_COUNT(self) -> int:
        """
        The maximum number of times the phone number can be changed after
        signup at the phone number verification stage.
        """
        pass

    @property
    def PHONE_VERIFICATION_MAX_RESEND_COUNT(self) -> int:
        """
        The maximum number of times the user can request a new phone number
        verification code.
        """
        pass

    @property
    def PHONE_VERIFICATION_TIMEOUT(self):
        pass

    @property
    def UNIQUE_EMAIL(self):
        """
        Enforce uniqueness of email addresses
        """
        pass

    @property
    def SIGNUP_EMAIL_ENTER_TWICE(self):
        """
        Signup email verification
        """
        pass

    @property
    def SIGNUP_PASSWORD_ENTER_TWICE(self):
        """
        Signup password verification
        """
        pass

    @property
    def SIGNUP_REDIRECT_URL(self):
        pass

    @property
    def PASSWORD_MIN_LENGTH(self):
        """
        Minimum password Length
        """
        pass

    @property
    def RATE_LIMITS(self):
        pass

    @property
    def EMAIL_SUBJECT_PREFIX(self):
        """
        Subject-line prefix to use for email messages sent
        """
        pass

    @property
    def SIGNUP_FORM_CLASS(self):
        """
        Signup form
        """
        pass

    @property
    def SIGNUP_FORM_HONEYPOT_FIELD(self):
        """
        Honeypot field name. Empty string or ``None`` will disable honeypot behavior.
        """
        pass

    @property
    def SIGNUP_FIELDS(self) -> dict:
        pass

    @property
    def USERNAME_REQUIRED(self):
        """
        The user is required to enter a username when signing up
        """
        pass

    @property
    def USERNAME_MIN_LENGTH(self):
        """
        Minimum username Length
        """
        pass

    @property
    def USERNAME_BLACKLIST(self):
        """
        List of usernames that are not allowed
        """
        pass

    @property
    def PASSWORD_INPUT_RENDER_VALUE(self):
        """
        render_value parameter as passed to PasswordInput fields
        """
        pass

    @property
    def ADAPTER(self):
        pass

    @property
    def CONFIRM_EMAIL_ON_GET(self):
        pass

    @property
    def AUTHENTICATED_LOGIN_REDIRECTS(self):
        pass

    @property
    def LOGIN_ON_EMAIL_CONFIRMATION(self):
        """
        Automatically log the user in once they confirmed their email address
        """
        pass

    @property
    def LOGIN_ON_PASSWORD_RESET(self):
        """
        Automatically log the user in immediately after resetting
        their password.
        """
        pass

    @property
    def LOGOUT_REDIRECT_URL(self):
        pass

    @property
    def LOGOUT_ON_GET(self):
        pass

    @property
    def LOGOUT_ON_PASSWORD_CHANGE(self):
        pass

    @property
    def USER_MODEL_USERNAME_FIELD(self):
        pass

    @property
    def USER_MODEL_EMAIL_FIELD(self):
        pass

    @property
    def SESSION_COOKIE_AGE(self):
        """
        Deprecated -- use Django's settings.SESSION_COOKIE_AGE instead
        """
        pass

    @property
    def SESSION_REMEMBER(self):
        """
        Controls the life time of the session. Set to `None` to ask the user
        ("Remember me?"), `False` to not remember, and `True` to always
        remember.
        """
        pass

    @property
    def TEMPLATE_EXTENSION(self):
        """
        A string defining the template extension to use, defaults to `html`.
        """
        pass

    @property
    def FORMS(self):
        pass

    @property
    def EMAIL_CONFIRMATION_HMAC(self):
        pass

    @property
    def SALT(self):
        pass

    @property
    def PRESERVE_USERNAME_CASING(self):
        pass

    @property
    def USERNAME_VALIDATORS(self):
        pass

    @property
    def PASSWORD_RESET_BY_CODE_ENABLED(self):
        pass

    @property
    def PASSWORD_RESET_BY_CODE_MAX_ATTEMPTS(self):
        pass

    @property
    def PASSWORD_RESET_BY_CODE_TIMEOUT(self):
        pass

    @property
    def PASSWORD_RESET_TOKEN_GENERATOR(self):
        from allauth.account.forms import EmailAwarePasswordResetTokenGenerator
        from allauth.utils import import_attribute

        token_generator_path = self._setting("PASSWORD_RESET_TOKEN_GENERATOR", None)
        if token_generator_path is not None:
            token_generator = import_attribute(token_generator_path)
        else:
            token_generator = EmailAwarePasswordResetTokenGenerator
        return token_generator

    @property
    def EMAIL_UNKNOWN_ACCOUNTS(self):
        pass

    @property
    def REAUTHENTICATION_TIMEOUT(self):
        pass

    @property
    def EMAIL_NOTIFICATIONS(self):
        pass

    @property
    def REAUTHENTICATION_REQUIRED(self):
        pass

    @property
    def LOGIN_BY_CODE_ENABLED(self):
        pass

    @property
    def LOGIN_BY_CODE_TRUST_ENABLED(self):
        pass

    @property
    def LOGIN_BY_CODE_MAX_ATTEMPTS(self):
        pass

    @property
    def LOGIN_BY_CODE_MAX_RESEND_COUNT(self) -> int:
        """
        The maximum number of times the user can request a new login code.
        """
        pass

    @property
    def LOGIN_BY_CODE_TIMEOUT(self):
        pass

    @property
    def LOGIN_TIMEOUT(self):
        """
        The maximum allowed time (in seconds) for a login to go through the
        various login stages. This limits, for example, the time span that the
        2FA stage remains available.
        """
        pass

    @property
    def LOGIN_BY_CODE_REQUIRED(self) -> bool | set[str]:
        """
        When enabled (in case of ``True``), every user logging in is
        required to input a login confirmation code sent by email.
        Alternatively, you can specify a set of authentication methods
        (``"password"``, ``"mfa"``, or ``"socialaccount"``) for which login
        codes are required.
        """
        pass

    @property
    def LOGIN_BY_CODE_FORMAT(self) -> UserCodeFormat:
        """
        Controls the format of the login code.
        """
        pass

    @property
    def PHONE_VERIFICATION_CODE_FORMAT(self) -> UserCodeFormat:
        """
        Controls the format of the phone verification code.
        """
        pass

    @property
    def PASSWORD_RESET_BY_CODE_FORMAT(self) -> UserCodeFormat:
        """
        Controls the format of the password reset code.
        """
        pass

    @property
    def EMAIL_VERIFICATION_BY_CODE_FORMAT(self) -> UserCodeFormat:
        """
        Controls the format of the email verification code.
        """
        pass


_app_settings = AppSettings("ACCOUNT_")


def __getattr__(name):
    # See https://peps.python.org/pep-0562/
    return getattr(_app_settings, name)
