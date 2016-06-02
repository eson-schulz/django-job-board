# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0006_auto_20160602_0013'),
    ]

    operations = [
        migrations.AlterField(
            model_name='company',
            name='plan',
            field=models.OneToOneField(to='account.Plan'),
        ),
    ]
