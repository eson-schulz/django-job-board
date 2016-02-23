# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0002_auto_20151108_2219'),
    ]

    operations = [
        migrations.AddField(
            model_name='company',
            name='stripe_id',
            field=models.CharField(max_length=50, null=True, blank=True),
        ),
    ]
