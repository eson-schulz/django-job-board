# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('board', '0020_auto_20160614_0150'),
    ]

    operations = [
        migrations.AlterField(
            model_name='post',
            name='application_details',
            field=models.CharField(max_length=600, null=True, blank=True),
        ),
    ]
