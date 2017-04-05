# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('volontulo', '0007_remove_page_slug'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='offerimage',
            name='userprofile',
        ),
    ]
