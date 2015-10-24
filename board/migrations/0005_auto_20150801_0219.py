# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('board', '0004_auto_20150726_2348'),
    ]

    operations = [
        migrations.AlterField(
            model_name='post',
            name='high_salary',
            field=models.IntegerField(null=True, blank=True),
        ),
        migrations.AlterField(
            model_name='post',
            name='low_salary',
            field=models.IntegerField(null=True, blank=True),
        ),
    ]
