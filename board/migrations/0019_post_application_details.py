# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('board', '0018_post_email'),
    ]

    operations = [
        migrations.AddField(
            model_name='post',
            name='application_details',
            field=models.CharField(max_length=300, null=True, blank=True),
        ),
    ]
