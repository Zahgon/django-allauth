from allauth.socialaccount.adapter import get_adapter
from allauth.socialaccount.providers.oauth2.views import (
    OAuth2Adapter,
    OAuth2CallbackView,
    OAuth2LoginView,
)


class CoinbaseOAuth2Adapter(OAuth2Adapter):
    provider_id = "coinbase"

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
        with get_adapter().get_requests_session() as sess:
            response = sess.get(self.profile_url, params={"access_token": token})
            extra_data = response.json()
        return self.get_provider().sociallogin_from_response(request, extra_data)


oauth2_login = OAuth2LoginView.adapter_view(CoinbaseOAuth2Adapter)
oauth2_callback = OAuth2CallbackView.adapter_view(CoinbaseOAuth2Adapter)
