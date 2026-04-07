from allauth.socialaccount.providers.base import ProviderAccount
from allauth.socialaccount.providers.oauth2.provider import OAuth2Provider
from allauth.socialaccount.providers.odnoklassniki.views import (
    OdnoklassnikiOAuth2Adapter,
)


class OdnoklassnikiAccount(ProviderAccount):
    def get_profile_url(self):
        pass

    def get_avatar_url(self):
        pass


class OdnoklassnikiProvider(OAuth2Provider):
    id = "odnoklassniki"
    name = "Odnoklassniki"
    account_class = OdnoklassnikiAccount
    oauth2_adapter_class = OdnoklassnikiOAuth2Adapter

    def extract_uid(self, data):
        return data["uid"]

    def extract_common_fields(self, data):
        return dict(
            last_name=data.get("last_name"),
            first_name=data.get("first_name"),
            email=data.get("email"),
        )


provider_classes = [OdnoklassnikiProvider]
