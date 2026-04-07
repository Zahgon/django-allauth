from django.core.checks import Critical, register


@register()
def settings_check(app_configs, **kwargs):
    pass
