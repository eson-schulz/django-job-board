# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('board', '0011_auto_20150804_1441'),
    ]

    operations = [
        migrations.AlterField(
            model_name='post',
            name='company',
            field=models.ForeignKey(to='account.Company'),
        ),
        migrations.DeleteModel(
            name='Company',
        ),
    ]
