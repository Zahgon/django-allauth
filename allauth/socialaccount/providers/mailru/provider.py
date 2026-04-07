from allauth.socialaccount.providers.base import ProviderAccount
from allauth.socialaccount.providers.mailru.views import MailRuOAuth2Adapter
from allauth.socialaccount.providers.oauth2.provider import OAuth2Provider


class MailRuAccount(ProviderAccount):
    def get_profile_url(self):
        pass

    def get_avatar_url(self):
        pass


class MailRuProvider(OAuth2Provider):
    id = "mailru"
    name = "Mail.RU"
    account_class = MailRuAccount
    oauth2_adapter_class = MailRuOAuth2Adapter

    def extract_uid(self, data):
        return data["uid"]

    def extract_common_fields(self, data):
        return dict(
            email=data.get("email"),
            last_name=data.get("last_name"),
            username=data.get("nick"),
            first_name=data.get("first_name"),
        )


provider_classes = [MailRuProvider]
