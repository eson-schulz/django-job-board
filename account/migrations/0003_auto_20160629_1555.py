# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0002_plan_slug'),
    ]

    operations = [
        migrations.AlterField(
            model_name='plan',
            name='slug',
            field=models.SlugField(unique=True),
        ),
    ]
