# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('board', '0010_auto_20150802_0319'),
    ]

    operations = [
        migrations.AddField(
            model_name='post',
            name='type_salary',
            field=models.CharField(blank=True, max_length=2, null=True, choices=[(b'HR', b'Hourly'), (b'DA', b'Daily'), (b'WK', b'Weekly'), (b'MO', b'Monthly'), (b'YR', b'Yearly')]),
        ),
        migrations.AlterField(
            model_name='company',
            name='picture',
            field=models.ImageField(upload_to=b'companies/', blank=True),
        ),
    ]
