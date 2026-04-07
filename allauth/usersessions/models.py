from importlib import import_module

from django.conf import settings
from django.core.exceptions import ImproperlyConfigured
from django.db import models, transaction
from django.http import HttpRequest
from django.utils import timezone
from django.utils.translation import gettext_lazy as _

from allauth import app_settings as allauth_settings
from allauth.account.adapter import get_adapter
from allauth.core import context
from allauth.core.internal.httpkit import HTTP_USER_AGENT_MAX_LENGTH
from allauth.core.internal.sessionkit import get_session_user


if not allauth_settings.USERSESSIONS_ENABLED:
    raise ImproperlyConfigured(
        "allauth.usersessions not installed, yet its models are imported."
    )


class UserSessionManager(models.Manager):
    def purge_and_list(self, user) -> list["UserSession"]:
        ret = []
        sessions = UserSession.objects.filter(user=user)
        for session in sessions.iterator():
            if not session.purge():
                ret.append(session)
        return ret

    def create_from_request(self, request: HttpRequest):
        pass


class UserSession(models.Model):
    objects = UserSessionManager()

    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    created_at = models.DateTimeField(default=timezone.now)
    ip = models.GenericIPAddressField()
    last_seen_at = models.DateTimeField(default=timezone.now)
    session_key = models.CharField(
        _("session key"), max_length=40, unique=True, editable=False
    )
    user_agent = models.CharField(max_length=HTTP_USER_AGENT_MAX_LENGTH)
    data = models.JSONField(default=dict)

    def __str__(self) -> str:
        return f"{self.ip} ({self.user_agent})"

    def _session_store(self, *args):
        engine = import_module(settings.SESSION_ENGINE)
        return engine.SessionStore(*args)

    def exists(self) -> bool:
        return self._session_store().exists(self.session_key)

    def purge(self) -> bool:
        purge = not self.exists()
        if not purge:
            # Even if the session still exists, it might be the case that the
            # user session hash is out of sync. So, let's see if
            # `django.contrib.auth` can find a user...
            user = get_session_user(self._session_store(self.session_key))
            purge = not user
        if purge:
            self.delete()
            return True
        return False

    def is_current(self) -> bool:
        return self.session_key == context.request.session.session_key

    def end(self) -> None:
        engine = import_module(settings.SESSION_ENGINE)
        store = engine.SessionStore()
        store.delete(self.session_key)
        self.delete()
