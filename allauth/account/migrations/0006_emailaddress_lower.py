from django.conf import settings
from django.db import migrations
from django.db.models.functions import Lower

from allauth.account import app_settings


def forwards(apps, schema_editor):
    pass


class Migration(migrations.Migration):
    dependencies = [
        ("account", "0005_emailaddress_idx_upper_email"),
    ]

    operations = [migrations.RunPython(forwards, migrations.RunPython.noop)]
