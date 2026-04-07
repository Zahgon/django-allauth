# Default locale mapping for the Facebook JS SDK
# The list of supported locales is at
# https://www.facebook.com/translations/FacebookLocales.xml
import os

from django.utils.translation import get_language, to_locale


def _build_locale_table(filename_or_file):
    """
    Parses the FacebookLocales.xml file and builds a dict relating every
    available language ('en, 'es, 'zh', ...) with a list of available regions
    for that language ('en' -> 'US', 'EN') and an (arbitrary) default region.
    """
    pass


def get_default_locale_callable():
    """
    Wrapper function so that the default mapping is only built when needed
    """
    pass
