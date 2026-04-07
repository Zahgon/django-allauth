from allauth.core import context
from allauth.socialaccount import app_settings
from allauth.socialaccount.adapter import get_adapter
from allauth.socialaccount.models import SocialToken
from allauth.socialaccount.providers.oauth2.views import (
    OAuth2Adapter,
    OAuth2CallbackView,
    OAuth2LoginView,
)


class NextCloudOAuth2Adapter(OAuth2Adapter):
    provider_id = "nextcloud"

    def _build_server_url(self, path):
        pass

    @property
    def access_token_url(self):
        pass

    @property
    def authorize_url(self):
        pass

    @property
    def profile_url(self):
        pass

    def complete_login(self, request, app, token: SocialToken, **kwargs):
        extra_data = self.get_user_info(token, kwargs["response"]["user_id"])
        return self.get_provider().sociallogin_from_response(request, extra_data)

    def get_user_info(self, token: SocialToken, user_id):
        headers = {"Authorization": f"Bearer {token.token}"}
        with get_adapter().get_requests_session() as sess:
            resp = sess.get(
                f"{self.profile_url}{user_id}",
                params={"format": "json"},
                headers=headers,
            )
            resp.raise_for_status()
            data = resp.json()["ocs"]["data"]
        return data


oauth2_login = OAuth2LoginView.adapter_view(NextCloudOAuth2Adapter)
oauth2_callback = OAuth2CallbackView.adapter_view(NextCloudOAuth2Adapter)
