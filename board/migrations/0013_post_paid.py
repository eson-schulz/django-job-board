# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('board', '0012_auto_20151024_1520'),
    ]

    operations = [
        migrations.AddField(
            model_name='post',
            name='paid',
            field=models.BooleanField(default=False),
        ),
    ]
