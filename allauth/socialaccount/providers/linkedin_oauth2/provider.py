from allauth.socialaccount import app_settings
from allauth.socialaccount.providers.base import ProviderAccount, ProviderException
from allauth.socialaccount.providers.linkedin_oauth2.views import LinkedInOAuth2Adapter
from allauth.socialaccount.providers.oauth2.provider import OAuth2Provider


def _extract_name_field(data, field_name):
    ret = ""
    v = data.get(field_name, {})
    if v:
        if isinstance(v, str):
            # Old V1 data
            ret = v
        else:
            localized = v.get("localized", {})
            preferred_locale = v.get(
                "preferredLocale", {"country": "US", "language": "en"}
            )
            locale_key = f"{preferred_locale['language']}_{preferred_locale['country']}"
            if locale_key in localized:
                ret = localized.get(locale_key)
            elif localized:
                ret = next(iter(localized.values()))
    return ret


def _extract_email(data):
    """
    {'elements': [{'handle': 'urn:li:emailAddress:319371470',
               'handle~': {'emailAddress': 'raymond.penners@intenct.nl'}}]}
    """
    ret = ""
    elements = data.get("elements", [])
    if len(elements) > 0:
        ret = elements[0].get("handle~", {}).get("emailAddress", "")
    return ret


class LinkedInOAuth2Account(ProviderAccount):
    def to_str(self):
        ret = super().to_str()
        if self.account.extra_data.get("emailAddress"):
            return self.account.extra_data["emailAddress"]
        first_name = _extract_name_field(self.account.extra_data, "firstName")
        last_name = _extract_name_field(self.account.extra_data, "lastName")
        if first_name or last_name:
            ret = f"{first_name} {last_name}".strip()
        return ret

    def get_avatar_url(self):
        """
        Attempts the load the avatar associated to the avatar.

        Requires the `profilePicture(displayImage~:playableStreams)`
        profile field configured in settings.py

        :return:
        """
        pass


class LinkedInOAuth2Provider(OAuth2Provider):
    id = "linkedin_oauth2"
    # Name is displayed to ordinary users -- don't include protocol
    name = "LinkedIn"
    account_class = LinkedInOAuth2Account
    oauth2_adapter_class = LinkedInOAuth2Adapter

    def extract_uid(self, data):
        if "id" not in data:
            raise ProviderException(
                "LinkedIn encountered an internal error while logging in. \
                Please try again."
            )
        return str(data["id"])

    def get_profile_fields(self):
        default_fields = [
            "id",
            "firstName",
            "lastName",
            # This would be needed to in case you need access to the image
            # URL. Not enabling this by default due to the amount of data
            # returned.
            #
            # 'profilePicture(displayImage~:playableStreams)'
        ]
        fields = self.get_settings().get("PROFILE_FIELDS", default_fields)
        return fields

    def get_default_scope(self):
        scope = ["r_liteprofile"]
        if app_settings.QUERY_EMAIL:
            scope.append("r_emailaddress")
        return scope

    def extract_common_fields(self, data):
        return dict(
            first_name=_extract_name_field(data, "firstName"),
            last_name=_extract_name_field(data, "lastName"),
            email=_extract_email(data),
        )


provider_classes = [LinkedInOAuth2Provider]
