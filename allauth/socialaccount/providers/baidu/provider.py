from allauth.socialaccount.providers.baidu.views import BaiduOAuth2Adapter
from allauth.socialaccount.providers.base import ProviderAccount
from allauth.socialaccount.providers.oauth2.provider import OAuth2Provider


class BaiduAccount(ProviderAccount):
    def get_profile_url(self):
        pass

    def get_avatar_url(self):
        pass

    def to_str(self):
        dflt = super().to_str()
        return self.account.extra_data.get("uname", dflt)


class BaiduProvider(OAuth2Provider):
    id = "baidu"
    name = "Baidu"
    account_class = BaiduAccount
    oauth2_adapter_class = BaiduOAuth2Adapter

    def extract_uid(self, data):
        return data["uid"]

    def extract_common_fields(self, data):
        return dict(username=data.get("uid"), name=data.get("uname"))


provider_classes = [BaiduProvider]
