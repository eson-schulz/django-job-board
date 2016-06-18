# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Category',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=80)),
                ('slug', models.SlugField(unique=True)),
            ],
            options={
                'verbose_name_plural': 'categories',
            },
        ),
        migrations.CreateModel(
            name='Post',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('title', models.CharField(max_length=60)),
                ('description', models.TextField()),
                ('date', models.DateField()),
                ('job_type', models.CharField(max_length=2, choices=[(b'FL', b'Full-time'), (b'PT', b'Part-time'), (b'CT', b'Contract'), (b'TY', b'Temporary'), (b'CN', b'Commission'), (b'IN', b'Internship')])),
                ('location', models.CharField(default=b'Owatonna, MN', max_length=30)),
                ('low_salary', models.IntegerField(null=True, blank=True)),
                ('high_salary', models.IntegerField(null=True, blank=True)),
                ('type_salary', models.CharField(blank=True, max_length=2, null=True, choices=[(b'HR', b'Hourly'), (b'DA', b'Daily'), (b'WK', b'Weekly'), (b'MO', b'Monthly'), (b'YR', b'Yearly')])),
                ('paid', models.BooleanField(default=False)),
                ('verified', models.BooleanField(default=False)),
                ('application_details', models.CharField(max_length=600, null=True, blank=True)),
                ('email', models.EmailField(max_length=254)),
                ('slug', models.SlugField(unique=True)),
                ('categories', models.ManyToManyField(to='board.Category', blank=True)),
                ('company', models.ForeignKey(to='account.Company')),
            ],
        ),
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=50)),
                ('resume', models.FileField(null=True, upload_to=b'', blank=True)),
                ('posts', models.ManyToManyField(to='board.Post')),
            ],
        ),
    ]
