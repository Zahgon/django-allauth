from django import forms
from django.utils.translation import gettext_lazy as _

from allauth.core import context
from allauth.mfa.adapter import get_adapter
from allauth.mfa.base.internal.flows import check_rate_limit, post_authentication
from allauth.mfa.models import Authenticator


class BaseAuthenticateForm(forms.Form):
    code = forms.CharField(
        label=_("Code"),
        widget=forms.TextInput(
            attrs={"placeholder": _("Code"), "autocomplete": "one-time-code"},
        ),
    )

    def __init__(self, *args, **kwargs) -> None:
        self.user = kwargs.pop("user")
        super().__init__(*args, **kwargs)

    def clean_code(self) -> str:
        pass


class AuthenticateForm(BaseAuthenticateForm):
    def save(self) -> None:
        post_authentication(context.request, self.authenticator)


class ReauthenticateForm(BaseAuthenticateForm):
    def save(self) -> None:
        post_authentication(context.request, self.authenticator, reauthenticated=True)
