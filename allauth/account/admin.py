from django.contrib import admin, messages
from django.utils.translation import gettext_lazy as _

from allauth.account import app_settings, signals
from allauth.account.adapter import get_adapter
from allauth.account.models import EmailAddress, EmailConfirmation


class EmailAddressAdmin(admin.ModelAdmin):
    list_display = ("email", "user", "primary", "verified")
    list_filter = ("primary", "verified")
    search_fields = []
    raw_id_fields = ("user",)
    actions = ["make_verified"]

    def get_search_fields(self, request):
        pass

    def make_verified(self, request, queryset):
        pass

    make_verified.short_description = _("Mark selected email addresses as verified")  # type: ignore[attr-defined]


class EmailConfirmationAdmin(admin.ModelAdmin):
    list_display = ("email_address", "created", "sent", "key")
    list_filter = ("sent",)
    raw_id_fields = ("email_address",)


if not app_settings.EMAIL_CONFIRMATION_HMAC:
    admin.site.register(EmailConfirmation, EmailConfirmationAdmin)
admin.site.register(EmailAddress, EmailAddressAdmin)
