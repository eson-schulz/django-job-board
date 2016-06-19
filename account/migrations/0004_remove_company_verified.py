# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0003_auto_20160619_0139'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='company',
            name='verified',
        ),
    ]
