from allauth.socialaccount.adapter import get_adapter
from allauth.socialaccount.providers.oauth2.views import (
    OAuth2Adapter,
    OAuth2CallbackView,
    OAuth2LoginView,
)


class RobinhoodOAuth2Adapter(OAuth2Adapter):
    provider_id = "robinhood"

    @property
    def authorize_url(self):
        pass

    @property
    def access_token_url(self):
        pass

    @property
    def profile_url(self):
        pass

    def complete_login(self, request, app, token, **kwargs):
        headers = {"Authorization": f"Bearer {token.token}"}
        with get_adapter().get_requests_session() as sess:
            response = sess.get(self.profile_url, headers=headers)
            extra_data = response.json()
        return self.get_provider().sociallogin_from_response(request, extra_data)


oauth2_login = OAuth2LoginView.adapter_view(RobinhoodOAuth2Adapter)
oauth2_callback = OAuth2CallbackView.adapter_view(RobinhoodOAuth2Adapter)
