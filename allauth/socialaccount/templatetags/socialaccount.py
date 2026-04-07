from django import template
from django.contrib.auth import REDIRECT_FIELD_NAME
from django.utils.safestring import mark_safe

from allauth.socialaccount.adapter import get_adapter
from allauth.utils import get_request_param


register = template.Library()


@register.simple_tag(takes_context=True)
def provider_login_url(context, provider, **params):
    """
    {% provider_login_url "facebook" next=bla %}
    {% provider_login_url "openid" openid="https://me.yahoo.com" next=bla %}
    """
    pass


@register.simple_tag(takes_context=True)
def providers_media_js(context):
    pass


@register.simple_tag
def get_social_accounts(user):
    """
    {% get_social_accounts user as accounts %}

    Then:
        {{accounts.twitter}} -- a list of connected Twitter accounts
        {{accounts.twitter.0}} -- the first Twitter account
        {% if accounts %} -- if there is at least one social account
    """
    pass


@register.simple_tag(takes_context=True)
def get_providers(context):
    """
    Returns a list of social authentication providers.

    Usage: `{% get_providers as socialaccount_providers %}`.

    Then within the template context, `socialaccount_providers` will hold
    a list of social providers configured for the current site.
    """
    pass
