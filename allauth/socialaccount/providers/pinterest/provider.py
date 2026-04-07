from allauth.socialaccount.providers.base import ProviderAccount
from allauth.socialaccount.providers.oauth2.provider import OAuth2Provider
from allauth.socialaccount.providers.pinterest.views import PinterestOAuth2Adapter


class PinterestAccount(ProviderAccount):
    def get_username(self):
        pass

    def get_profile_url(self):
        # v5 extra_data not same as v1
        pass

    def get_avatar_url(self):
        pass


class PinterestProvider(OAuth2Provider):
    id = "pinterest"
    name = "Pinterest"
    account_class = PinterestAccount
    oauth2_adapter_class = PinterestOAuth2Adapter

    @property
    def api_version(self):
        pass

    def get_default_scope(self):
        # See: https://developers.pinterest.com/docs/api/overview/#scopes
        if self.api_version == "v5":
            # See: https://developers.pinterest.com/docs/getting-started/scopes/
            return ["user_accounts:read"]
        elif self.api_version == "v3":
            return ["read_users"]
        return ["read_public"]

    def extract_extra_data(self, data):
        if self.api_version == "v5":
            return data
        return data.get("data", {})

    def extract_uid(self, data):
        if self.api_version == "v5":
            return data["username"]
        return str(data["data"]["id"])

    def extract_common_fields(self, data):
        if self.api_version == "v5":
            return dict(username=data["username"])
        return dict(
            first_name=data.get("data", {}).get("first_name"),
            last_name=data.get("data", {}).get("last_name"),
        )


provider_classes = [PinterestProvider]
