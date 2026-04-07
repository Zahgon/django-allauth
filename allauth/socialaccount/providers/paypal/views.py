from allauth.socialaccount.adapter import get_adapter
from allauth.socialaccount.providers.oauth2.views import (
    OAuth2Adapter,
    OAuth2CallbackView,
    OAuth2LoginView,
)


class PaypalOAuth2Adapter(OAuth2Adapter):
    provider_id = "paypal"

    @property
    def authorize_url(self):
        pass

    @property
    def access_token_url(self):
        pass

    @property
    def profile_url(self):
        pass

    def _get_endpoint(self):
        pass

    def complete_login(self, request, app, token, **kwargs):
        with get_adapter().get_requests_session() as sess:
            response = sess.post(
                self.profile_url,
                params={"schema": "openid", "access_token": token.token},
            )
            extra_data = response.json()
        return self.get_provider().sociallogin_from_response(request, extra_data)


oauth2_login = OAuth2LoginView.adapter_view(PaypalOAuth2Adapter)
oauth2_callback = OAuth2CallbackView.adapter_view(PaypalOAuth2Adapter)
