# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0004_company_max_posts'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='company',
            name='max_posts',
        ),
        migrations.AddField(
            model_name='company',
            name='plan',
            field=models.CharField(default=b'B', max_length=1, choices=[(b'B', b'Basic'), (b'A', b'Advanced'), (b'P', b'Premium'), (b'C', b'Custom')]),
        ),
    ]
