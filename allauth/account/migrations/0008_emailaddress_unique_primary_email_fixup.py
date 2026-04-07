from django.conf import settings
from django.db import migrations
from django.db.models import Count


def forwards(apps, schema_editor):
    pass


class Migration(migrations.Migration):
    dependencies = [
        ("account", "0007_emailaddress_idx_email"),
    ]

    operations = [
        migrations.RunPython(code=forwards, reverse_code=migrations.RunPython.noop)
    ]
