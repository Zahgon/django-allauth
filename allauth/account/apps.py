from django.apps import AppConfig
from django.conf import settings
from django.core.exceptions import ImproperlyConfigured
from django.utils.translation import gettext_lazy as _

from allauth import app_settings


class AccountConfig(AppConfig):
    name = "allauth.account"
    verbose_name = _("Accounts")
    default_auto_field = app_settings.DEFAULT_AUTO_FIELD or "django.db.models.AutoField"

    def ready(self):
        pass
