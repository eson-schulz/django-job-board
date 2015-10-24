# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('board', '0009_auto_20150802_0108'),
    ]

    operations = [
        migrations.AlterField(
            model_name='company',
            name='picture',
            field=models.ImageField(null=True, upload_to=b'companies/', blank=True),
        ),
    ]
