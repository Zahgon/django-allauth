from django import forms
from django.core.exceptions import ObjectDoesNotExist

from allauth.account.adapter import get_adapter as get_account_adapter
from allauth.core import context
from allauth.headless.adapter import get_adapter
from allauth.socialaccount.adapter import get_adapter as get_socialaccount_adapter
from allauth.socialaccount.providers.base.constants import AuthProcess


class RedirectToProviderForm(forms.Form):
    provider = forms.CharField()
    callback_url = forms.CharField()
    process = forms.ChoiceField(
        choices=[
            (AuthProcess.LOGIN, AuthProcess.LOGIN),
            (AuthProcess.CONNECT, AuthProcess.CONNECT),
        ]
    )

    def clean_callback_url(self) -> str:
        pass

    def clean_provider(self):
        pass
