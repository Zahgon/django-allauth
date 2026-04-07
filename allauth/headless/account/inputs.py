from django.core.exceptions import ValidationError
from django.core.validators import validate_email

from allauth.account import app_settings as account_settings
from allauth.account.adapter import get_adapter as get_account_adapter
from allauth.account.fields import PhoneField
from allauth.account.forms import (
    AddEmailForm,
    BaseSignupForm,
    ChangeEmailForm,
    ChangePhoneForm,
    ConfirmLoginCodeForm,
    ReauthenticateForm,
    RequestLoginCodeForm,
    ResetPasswordForm,
    UserTokenForm,
    VerifyPhoneForm,
)
from allauth.account.internal import flows
from allauth.account.models import EmailAddress, Login, get_emailconfirmation_model
from allauth.core import context
from allauth.core.internal.cryptokit import compare_user_code
from allauth.headless.adapter import get_adapter
from allauth.headless.internal.restkit import inputs


class SignupInput(BaseSignupForm, inputs.Input):
    password = inputs.CharField()

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        password = account_settings.SIGNUP_FIELDS.get("password1")
        if not password:
            del self.fields["password"]
        else:
            self.fields["password"].required = password["required"]

    def clean_password(self):
        password = self.cleaned_data["password"]
        if password:
            return get_account_adapter().clean_password(password)
        return password


class LoginInput(inputs.Input):
    username = inputs.CharField(required=False)
    email = inputs.EmailField(required=False)
    # NOTE: Always require E164, no need to use adapter.phone_form_field
    phone = PhoneField(required=False)
    password = inputs.CharField()

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in ["username", "email", "phone"]:
            if field not in account_settings.LOGIN_METHODS:
                del self.fields[field]
        if len(account_settings.LOGIN_METHODS) == 1:
            self.fields[next(iter(account_settings.LOGIN_METHODS))].required = True

    def clean(self):
        cleaned_data = super().clean()
        if self.errors:
            return cleaned_data
        credentials = {}
        for login_method in account_settings.LOGIN_METHODS:
            value = cleaned_data.get(login_method)
            if value is not None and login_method in self.data.keys():
                credentials[login_method] = value
        if len(credentials) != 1:
            raise get_account_adapter().validation_error("invalid_login")
        password = cleaned_data.get("password")
        if password:
            auth_method = next(iter(credentials.keys()))
            credentials["password"] = password
            user = get_account_adapter().authenticate(context.request, **credentials)
            if user:
                self.login = Login(user=user, email=credentials.get("email"))
                if flows.login.is_login_rate_limited(context.request, self.login):
                    raise get_account_adapter().validation_error(
                        "too_many_login_attempts"
                    )
            else:
                error_code = f"{auth_method.value}_password_mismatch"
                self.add_error(
                    "password", get_account_adapter().validation_error(error_code)
                )
        return cleaned_data


class VerifyEmailInput(inputs.Input):
    key = inputs.CharField()

    def __init__(self, *args, **kwargs):
        self.process = kwargs.pop("process", None)
        super().__init__(*args, **kwargs)

    def clean_key(self):
        pass


class RequestPasswordResetInput(ResetPasswordForm, inputs.Input):
    pass


class ResetPasswordKeyInput(inputs.Input):
    key = inputs.CharField()

    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop("user", None)
        self.code = kwargs.pop("code", None)
        super().__init__(*args, **kwargs)

    def clean_key(self):
        pass

    def _clean_key_code(self):
        pass

    def _clean_key_link(self):
        pass


class ResetPasswordInput(ResetPasswordKeyInput):
    password = inputs.CharField()

    def clean(self):
        cleaned_data = super().clean()
        password = self.cleaned_data.get("password")
        if self.user and password is not None:
            try:
                get_account_adapter().clean_password(password, user=self.user)
            except ValidationError as e:
                self.add_error("password", e)
        return cleaned_data


class ChangePasswordInput(inputs.Input):
    current_password = inputs.CharField(required=False)
    new_password = inputs.CharField()

    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop("user")
        super().__init__(*args, **kwargs)
        self.fields["current_password"].required = self.user.has_usable_password()

    def clean_current_password(self):
        pass

    def clean_new_password(self):
        pass


class AddEmailInput(AddEmailForm, inputs.Input):
    pass


class SelectEmailInput(inputs.Input):
    email = inputs.CharField()

    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop("user")
        super().__init__(*args, **kwargs)

    def clean_email(self):
        self.process = None
        email = self.cleaned_data["email"]
        validate_email(email)

        # Select a database backed email...
        try:
            return EmailAddress.objects.get_for_user(user=self.user, email=email)
        except EmailAddress.DoesNotExist:
            pass

        # Or, if email verification by code is active, try the pending email
        request = context.request
        self.process = flows.email_verification_by_code.EmailVerificationProcess.resume(
            request
        )
        if self.process:
            email_address = self.process.email_address
            if email_address.email.lower() == email.lower() and (
                request.user.is_anonymous or email_address.user_id == request.user.pk
            ):
                return email_address

        raise get_adapter().validation_error("unknown_email")


class DeleteEmailInput(SelectEmailInput):
    def clean_email(self):
        email = super().clean_email()
        if not flows.manage_email.can_delete_email(email):
            raise get_account_adapter().validation_error("cannot_remove_primary_email")
        return email


class MarkAsPrimaryEmailInput(SelectEmailInput):
    primary = inputs.BooleanField(required=True)

    def clean_email(self):
        email = super().clean_email()
        if not flows.manage_email.can_mark_as_primary(email):
            raise get_account_adapter().validation_error("unverified_primary_email")
        return email


class ResendEmailVerificationInput(SelectEmailInput):
    pass


class ReauthenticateInput(ReauthenticateForm, inputs.Input):
    pass


class RequestLoginCodeInput(RequestLoginCodeForm, inputs.Input):
    pass


class ConfirmLoginCodeInput(ConfirmLoginCodeForm, inputs.Input):
    pass


class VerifyPhoneInput(VerifyPhoneForm, inputs.Input):
    pass


class ChangePhoneInput(ChangePhoneForm, inputs.Input):
    pass


class ChangeEmailInput(ChangeEmailForm, inputs.Input):
    pass
