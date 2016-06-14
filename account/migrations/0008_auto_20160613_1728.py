# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0007_auto_20160602_0023'),
    ]

    operations = [
        migrations.AddField(
            model_name='plan',
            name='company_image',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='plan',
            name='email_post',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='plan',
            name='social_links',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='plan',
            name='social_post',
            field=models.BooleanField(default=False),
        ),
    ]
