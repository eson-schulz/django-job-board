# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='company',
            name='facebook_url',
            field=models.CharField(max_length=200, blank=True),
        ),
        migrations.AddField(
            model_name='company',
            name='twitter_url',
            field=models.CharField(max_length=200, blank=True),
        ),
        migrations.AddField(
            model_name='company',
            name='verified',
            field=models.BooleanField(default=False),
        ),
    ]
