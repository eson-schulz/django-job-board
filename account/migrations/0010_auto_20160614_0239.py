# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0009_plan_visible'),
    ]

    operations = [
        migrations.AlterField(
            model_name='company',
            name='plan',
            field=models.ForeignKey(to='account.Plan'),
        ),
    ]
