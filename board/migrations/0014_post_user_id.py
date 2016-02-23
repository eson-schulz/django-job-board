# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('board', '0013_post_paid'),
    ]

    operations = [
        migrations.AddField(
            model_name='post',
            name='user_id',
            field=models.CharField(default=b'Invalid', max_length=50),
        ),
    ]
