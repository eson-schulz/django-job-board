# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0002_auto_20160619_0137'),
    ]

    operations = [
        migrations.AlterField(
            model_name='company',
            name='facebook_url',
            field=models.URLField(blank=True),
        ),
        migrations.AlterField(
            model_name='company',
            name='twitter_url',
            field=models.URLField(blank=True),
        ),
    ]
