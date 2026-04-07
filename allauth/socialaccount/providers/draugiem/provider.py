from django.urls import reverse
from django.utils.http import urlencode

from allauth.socialaccount.providers.base import Provider, ProviderAccount


class DraugiemAccount(ProviderAccount):
    def get_avatar_url(self):
        pass


class DraugiemProvider(Provider):
    id = "draugiem"
    name = "Draugiem"
    account_class = DraugiemAccount

    def get_login_url(self, request, **kwargs):
        url = reverse(f"{self.id}_login")
        if kwargs:
            url = f"{url}?{urlencode(kwargs)}"
        return url

    def extract_uid(self, data):
        return str(data["uid"])

    def extract_common_fields(self, data):
        uid = self.extract_uid(data)
        user_data = data["users"][uid]
        return dict(
            first_name=user_data.get("name"),
            last_name=user_data.get("surname"),
        )

    def extract_extra_data(self, data):
        uid = self.extract_uid(data)
        return data["users"][uid]


provider_classes = [DraugiemProvider]
