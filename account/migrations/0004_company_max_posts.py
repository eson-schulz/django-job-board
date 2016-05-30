# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0003_company_stripe_id'),
    ]

    operations = [
        migrations.AddField(
            model_name='company',
            name='max_posts',
            field=models.SmallIntegerField(default=2),
        ),
    ]
