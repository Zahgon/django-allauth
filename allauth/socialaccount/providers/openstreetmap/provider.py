from allauth.socialaccount.providers.base import ProviderAccount
from allauth.socialaccount.providers.oauth.provider import OAuthProvider
from allauth.socialaccount.providers.openstreetmap.views import (
    OpenStreetMapOAuthAdapter,
)


class OpenStreetMapAccount(ProviderAccount):
    def get_profile_url(self):
        pass

    def get_avatar_url(self):
        pass

    def get_username(self):
        pass


class OpenStreetMapProvider(OAuthProvider):
    id = "openstreetmap"
    name = "OpenStreetMap"
    account_class = OpenStreetMapAccount
    oauth_adapter_class = OpenStreetMapOAuthAdapter

    def extract_uid(self, data):
        return str(data["id"])

    def extract_common_fields(self, data):
        return dict(username=data["display_name"])


provider_classes = [OpenStreetMapProvider]
