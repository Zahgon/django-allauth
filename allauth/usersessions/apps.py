from django.apps import AppConfig
from django.utils.translation import gettext_lazy as _

from allauth import app_settings


class UserSessionsConfig(AppConfig):
    name = "allauth.usersessions"
    verbose_name = _("User Sessions")
    default_auto_field = (
        app_settings.DEFAULT_AUTO_FIELD or "django.db.models.BigAutoField"
    )

    def ready(self):
        pass
