# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0005_auto_20160601_1829'),
    ]

    operations = [
        migrations.CreateModel(
            name='Plan',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=20)),
                ('stripe_id', models.CharField(max_length=20)),
                ('max_posts', models.PositiveSmallIntegerField()),
                ('max_upgraded_posts', models.PositiveSmallIntegerField()),
                ('cost', models.PositiveSmallIntegerField()),
            ],
        ),
        migrations.AlterField(
            model_name='company',
            name='plan',
            field=models.OneToOneField(null=True, to='account.Plan'),
        ),
    ]
