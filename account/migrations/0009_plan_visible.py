# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0008_auto_20160613_1728'),
    ]

    operations = [
        migrations.AddField(
            model_name='plan',
            name='visible',
            field=models.BooleanField(default=True),
        ),
    ]
