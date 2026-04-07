from django.core.checks import Critical, Warning, register


@register()
def adapter_check(app_configs, **kwargs):
    pass


@register()
def settings_check(app_configs, **kwargs):
    pass
