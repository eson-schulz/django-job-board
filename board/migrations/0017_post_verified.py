# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('board', '0016_remove_post_user_id'),
    ]

    operations = [
        migrations.AddField(
            model_name='post',
            name='verified',
            field=models.BooleanField(default=False),
        ),
    ]
