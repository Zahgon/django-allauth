import hashlib

from allauth.account.models import EmailAddress
from allauth.socialaccount.providers.base import ProviderAccount
from allauth.socialaccount.providers.frontier.views import FrontierOAuth2Adapter
from allauth.socialaccount.providers.oauth2.provider import OAuth2Provider


class FrontierAccount(ProviderAccount):
    def get_profile_url(self):
        pass

    def get_avatar_url(self):
        pass


class FrontierProvider(OAuth2Provider):
    id = "frontier"
    name = "Frontier"
    account_class = FrontierAccount
    oauth2_adapter_class = FrontierOAuth2Adapter

    def get_default_scope(self):
        scope = ["auth", "capi"]
        return scope

    def extract_uid(self, data):
        return str(data["customer_id"])

    def extract_common_fields(self, data):
        return dict(
            email=data.get("email"),
            username=data.get("email"),
            last_name=data.get("lastname"),
            first_name=data.get("firstname"),
        )

    def extract_email_addresses(self, data):
        ret = []
        email = data.get("email")
        if email:
            ret.append(EmailAddress(email=email, verified=True, primary=True))
        return ret


provider_classes = [FrontierProvider]
