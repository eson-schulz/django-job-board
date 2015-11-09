# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='company',
            name='description',
            field=models.TextField(blank=True),
        ),
        migrations.AlterField(
            model_name='company',
            name='location',
            field=models.CharField(default=b'Owatonna, MN', max_length=30, blank=True),
        ),
        migrations.AlterField(
            model_name='company',
            name='website',
            field=models.URLField(blank=True),
        ),
    ]
